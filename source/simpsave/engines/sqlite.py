"""
@file sqlite.py
@author WaterRun
@version 10
@date 2025-11-07
@description SQLITE engine for SimpSave
"""

import os
import re
import sqlite3
from .base import BaseEngine
from ..utils import validate_basic_type, serialize_value, deserialize_value


class SqliteEngine(BaseEngine):
    r"""
    SQLITE Engine
    """

    @classmethod
    def check_available(cls) -> bool:
        return True  # sqlite3 is in standard library

    @classmethod
    def get_default_suffix(cls) -> str:
        return '.db'

    def _get_connection(self, file: str) -> sqlite3.Connection:
        r"""
        Get database connection and ensure table exists
        :param file: Database file path
        :return: Database connection
        """
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simpsave (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        conn.commit()
        return conn

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__

        try:
            value = serialize_value(value)
            value_str = repr(value)
            
            conn = self._get_connection(file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO simpsave (key, value, type)
                VALUES (?, ?, ?)
            ''', (key, value_str, value_type))
            
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified database does not exist: {file}')
        
        conn = self._get_connection(file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT value, type FROM simpsave WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        if result is None:
            raise KeyError(f'Key {key} does not exist in database {file}')
        
        value_str, type_str = result
        value = eval(value_str)
        return deserialize_value(value, type_str)

    def has(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        
        conn = self._get_connection(file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM simpsave WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        return result is not None

    def remove(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        
        conn = self._get_connection(file)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM simpsave WHERE key = ?', (key,))
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def match(self, regex: str, file: str) -> dict:
        if not os.path.isfile(file):
            return {}
        
        conn = self._get_connection(file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT key FROM simpsave')
        keys = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        pattern = re.compile(regex)
        result = {}
        for key in keys:
            if pattern.match(key):
                result[key] = self.read(key, file)
        
        return result

    def delete(self, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        try:
            os.remove(file)
            return True
        except IOError:
            return False
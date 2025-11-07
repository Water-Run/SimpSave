"""
@file file.py
@author WaterRun
@version 10
@date 2025-11-07
@description SIMP engine for SimpSave (ultra-minimal, no dependencies)
"""

import os
import re
from .base import BaseEngine
from ..utils import validate_basic_type, ensure_file_exists, serialize_value, deserialize_value


class SimpEngine(BaseEngine):
    r"""
    SIMP File Engine
    """

    @classmethod
    def check_available(cls) -> bool:
        return True

    @classmethod
    def get_default_suffix(cls) -> str:
        return '.simpsave'

    def _load_file(self, file: str) -> dict:
        r"""
        Load data from file
        :param file: File path
        :return: Dictionary of data
        """
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified file does not exist: {file}')
        
        data = {}
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|', 2)
                if len(parts) == 3:
                    key, type_str, value_str = parts
                    # Simple eval for basic types (safe for controlled data)
                    try:
                        value = eval(value_str)
                        data[key] = {'value': value, 'type': type_str}
                    except Exception:
                        continue
        return data

    def _dump_file(self, data: dict, file: str) -> None:
        r"""
        Dump data to file
        :param data: Dictionary of data
        :param file: File path
        """
        with open(file, 'w', encoding='utf-8') as f:
            for key, val in data.items():
                value = val['value']
                type_str = val['type']
                value_str = repr(value)
                f.write(f"{key}|{type_str}|{value_str}\n")

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__
        ensure_file_exists(file)

        try:
            data = {}
            if os.path.exists(file) and os.path.getsize(file) > 0:
                try:
                    data = self._load_file(file)
                except Exception:
                    data = {}

            value = serialize_value(value)
            data[key] = {'value': value, 'type': value_type}
            self._dump_file(data, file)
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        data = self._load_file(file)
        if key not in data:
            raise KeyError(f'Key {key} does not exist in file {file}')
        val = data[key]
        return deserialize_value(val['value'], val['type'])

    def has(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_file(file)
        return key in data

    def remove(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_file(file)
        if key not in data:
            return False
        data.pop(key)
        self._dump_file(data, file)
        return True

    def match(self, regex: str, file: str) -> dict:
        if not os.path.isfile(file):
            return {}
        data = self._load_file(file)
        pattern = re.compile(regex)
        result = {}
        for k in data:
            if pattern.match(k):
                result[k] = self.read(k, file)
        return result

    def delete(self, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        try:
            os.remove(file)
            return True
        except IOError:
            return False
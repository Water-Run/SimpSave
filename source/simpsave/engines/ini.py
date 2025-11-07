"""
@file ini.py
@author WaterRun
@version 10
@date 2025-11-07
@description INI engine for SimpSave
"""

import os
import re
import configparser
from .base import BaseEngine
from ..utils import validate_basic_type, ensure_file_exists, serialize_value, deserialize_value


class IniEngine(BaseEngine):
    r"""
    INI Engine
    """

    SECTION_NAME = 'simpsave'

    @classmethod
    def check_available(cls) -> bool:
        return True  # configparser is in standard library

    @classmethod
    def get_default_suffix(cls) -> str:
        return '.ini'

    def _load_ini(self, file: str) -> dict:
        r"""
        Load the INI file
        :param file: Path to the INI file
        :return: Loaded dict object
        """
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .ini file does not exist: {file}')
        
        config = configparser.ConfigParser()
        config.read(file, encoding='utf-8')
        
        data = {}
        if config.has_section(self.SECTION_NAME):
            for key in config[self.SECTION_NAME]:
                value_str = config[self.SECTION_NAME][key]
                # Parse format: type|value
                parts = value_str.split('|', 1)
                if len(parts) == 2:
                    type_str, val_str = parts
                    try:
                        value = eval(val_str)
                        data[key] = {'value': value, 'type': type_str}
                    except Exception:
                        continue
        return data

    def _dump_ini(self, data: dict, file: str) -> None:
        r"""
        Dump data to INI file
        :param data: Dictionary of data
        :param file: File path
        """
        config = configparser.ConfigParser()
        config.add_section(self.SECTION_NAME)
        
        for key, val in data.items():
            value = val['value']
            type_str = val['type']
            value_str = repr(value)
            config[self.SECTION_NAME][key] = f"{type_str}|{value_str}"
        
        with open(file, 'w', encoding='utf-8') as f:
            config.write(f)

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__
        ensure_file_exists(file)

        try:
            data = {}
            if os.path.exists(file) and os.path.getsize(file) > 0:
                try:
                    data = self._load_ini(file)
                except Exception:
                    data = {}

            value = serialize_value(value)
            data[key] = {'value': value, 'type': value_type}
            self._dump_ini(data, file)
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        data = self._load_ini(file)
        if key not in data:
            raise KeyError(f'Key {key} does not exist in file {file}')
        val = data[key]
        return deserialize_value(val['value'], val['type'])

    def has(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_ini(file)
        return key in data

    def remove(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_ini(file)
        if key not in data:
            return False
        data.pop(key)
        self._dump_ini(data, file)
        return True

    def match(self, regex: str, file: str) -> dict:
        if not os.path.isfile(file):
            return {}
        data = self._load_ini(file)
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
"""
@file toml.py
@author WaterRun
@version 10
@date 2025-11-07
@description TOML engine for SimpSave
"""

import os
import re
import sys
from .base import BaseEngine
from ..utils import validate_basic_type, ensure_file_exists, serialize_value, deserialize_value


class TomlEngine(BaseEngine):
    r"""
    TOML Engine
    """

    @classmethod
    def check_available(cls) -> bool:
        try:
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib
            import tomli_w
            return True
        except ImportError:
            return False

    @classmethod
    def get_default_suffix(cls) -> str:
        return '.toml'

    def _load_toml(self, file: str) -> dict:
        r"""
        Load the TOML file
        :param file: Path to the TOML file
        :return: Loaded dict object
        """
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib
        
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .toml file does not exist: {file}')
        
        with open(file, 'rb') as f:
            data = tomllib.load(f)
        return data if isinstance(data, dict) else {}

    def _dump_toml(self, data: dict, file: str) -> None:
        r"""
        Dump data to TOML file
        :param data: Dictionary of data
        :param file: File path
        """
        import tomli_w
        
        with open(file, 'wb') as f:
            tomli_w.dump(data, f)

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__
        ensure_file_exists(file)

        try:
            data = {}
            if os.path.exists(file) and os.path.getsize(file) > 0:
                try:
                    data = self._load_toml(file)
                except Exception:
                    data = {}

            value = serialize_value(value)
            data[key] = {'value': value, 'type': value_type}
            self._dump_toml(data, file)
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        data = self._load_toml(file)
        if key not in data:
            raise KeyError(f'Key {key} does not exist in file {file}')
        val = data[key]
        return deserialize_value(val['value'], val['type'])

    def has(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_toml(file)
        return key in data

    def remove(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_toml(file)
        if key not in data:
            return False
        data.pop(key)
        self._dump_toml(data, file)
        return True

    def match(self, regex: str, file: str) -> dict:
        if not os.path.isfile(file):
            return {}
        data = self._load_toml(file)
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
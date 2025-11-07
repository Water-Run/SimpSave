"""
@file yml.py
@author WaterRun
@version 10
@date 2025-11-07
@description YML engine for SimpSave
"""

import os
import re
from .base import BaseEngine
from ..utils import validate_basic_type, ensure_file_exists, serialize_value, deserialize_value


class YmlEngine(BaseEngine):
    r"""
    YML Engine
    """

    @classmethod
    def check_available(cls) -> bool:
        try:
            import yaml
            return True
        except ImportError:
            return False

    @classmethod
    def get_default_suffix(cls) -> str:
        return '.yml'

    def _load_yaml(self, file: str) -> dict:
        r"""
        Load the YAML file
        :param file: Path to the YAML file
        :return: Loaded dict object
        :raise FileNotFoundError: If the file does not exist
        """
        import yaml
        
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .yml file does not exist: {file}')
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        data = yaml.safe_load(content)
        return data if isinstance(data, dict) else {}

    def _dump_yaml(self, data: dict, file: str) -> None:
        r"""
        Dump data to YAML file
        :param data: Dictionary of data
        :param file: File path
        """
        import yaml
        
        with open(file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__
        ensure_file_exists(file)

        try:
            data = {}
            if os.path.exists(file) and os.path.getsize(file) > 0:
                try:
                    data = self._load_yaml(file)
                except Exception:
                    data = {}

            value = serialize_value(value)
            data[key] = {'value': value, 'type': value_type}
            self._dump_yaml(data, file)
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        data = self._load_yaml(file)
        if key not in data:
            raise KeyError(f'Key {key} does not exist in file {file}')
        val = data[key]
        return deserialize_value(val['value'], val['type'])

    def has(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_yaml(file)
        return key in data

    def remove(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_yaml(file)
        if key not in data:
            return False
        data.pop(key)
        self._dump_yaml(data, file)
        return True

    def match(self, regex: str, file: str) -> dict:
        if not os.path.isfile(file):
            return {}
        data = self._load_yaml(file)
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
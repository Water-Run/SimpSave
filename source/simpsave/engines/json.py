"""
@file json.py
@author WaterRun
@version 10
@date 2025-11-07
@description JSON engine for SimpSave
"""

import os
import re
import json
from .base import BaseEngine
from ..utils import validate_basic_type, ensure_file_exists, serialize_value, deserialize_value


class JsonEngine(BaseEngine):
    r"""
    JSON Engine
    """

    @classmethod
    def check_available(cls) -> bool:
        return True  # json is in standard library

    @classmethod
    def get_default_suffix(cls) -> str:
        return '.json'

    def _load_json(self, file: str) -> dict:
        r"""
        Load the JSON file
        :param file: Path to the JSON file
        :return: Loaded dict object
        """
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .json file does not exist: {file}')
        
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}

    def _dump_json(self, data: dict, file: str) -> None:
        r"""
        Dump data to JSON file
        :param data: Dictionary of data
        :param file: File path
        """
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__
        ensure_file_exists(file)

        try:
            data = {}
            if os.path.exists(file) and os.path.getsize(file) > 0:
                try:
                    data = self._load_json(file)
                except Exception:
                    data = {}

            value = serialize_value(value)
            data[key] = {'value': value, 'type': value_type}
            self._dump_json(data, file)
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        data = self._load_json(file)
        if key not in data:
            raise KeyError(f'Key {key} does not exist in file {file}')
        val = data[key]
        return deserialize_value(val['value'], val['type'])

    def has(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_json(file)
        return key in data

    def remove(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        data = self._load_json(file)
        if key not in data:
            return False
        data.pop(key)
        self._dump_json(data, file)
        return True

    def match(self, regex: str, file: str) -> dict:
        if not os.path.isfile(file):
            return {}
        data = self._load_json(file)
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
"""
@file utils.py
@author WaterRun
@version 10
@date 2025-11-07
@description Utility functions for SimpSave
"""

import os
import importlib.util
from .exceptions import InvalidPathError


def validate_basic_type(value):
    r"""
    Validate that a value and all its nested elements are Python basic types
    :param value: Value to validate
    :raise TypeError: If the value or its elements are not basic types
    """
    basic_types = (int, float, str, bool, bytes, complex, list, tuple, set, frozenset, dict, type(None))
    
    if isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            if not isinstance(item, basic_types):
                raise TypeError(f"All elements in {type(value).__name__} must be Python basic types.")
            validate_basic_type(item)
    elif isinstance(value, dict):
        for k, v in value.items():
            if not isinstance(k, basic_types) or not isinstance(v, basic_types):
                raise TypeError("All keys and values in a dict must be Python basic types.")
            validate_basic_type(v)
    elif not isinstance(value, basic_types):
        raise TypeError(f"Value must be a Python basic type, got {type(value).__name__} instead.")


def parse_path(path: str | None, default_suffix: str) -> str:
    r"""
    Handle and convert paths
    :param path: Path to be processed
    :param default_suffix: Default file suffix if path is None
    :return: Processed absolute path
    :raise InvalidPathError: If the path is not a string or is invalid
    :raise ImportError: If using :ss: and not installed via pip
    """
    if path is None:
        path = f'__ss__{default_suffix}'

    if not isinstance(path, str):
        raise InvalidPathError("Path must be a string")

    if path.startswith(':ss:'):
        spec = importlib.util.find_spec("simpsave")
        if spec is None:
            raise ImportError("When using the 'ss' directive, simpsave must be installed via pip")
        simpsave_path = os.path.join(spec.submodule_search_locations[0])
        relative_path = path[len(':ss:'):]
        return os.path.join(simpsave_path, relative_path)

    absolute_path = os.path.abspath(path)

    if not os.path.isfile(absolute_path) and not os.path.isdir(os.path.dirname(absolute_path)):
        raise InvalidPathError(f"Invalid path in the system: {absolute_path}")

    return absolute_path


def ensure_file_exists(file: str) -> None:
    r"""
    Ensure the file exists, create it if it doesn't
    :param file: File path
    """
    if not os.path.exists(file):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w', encoding='utf-8') as f:
            f.write("")


def serialize_value(value):
    r"""
    Serialize special types for storage
    :param value: Value to serialize
    :return: Serialized value
    """
    if isinstance(value, set):
        return list(value)
    elif isinstance(value, frozenset):
        return list(value)
    elif isinstance(value, bytes):
        return list(value)
    return value


def deserialize_value(value, type_str: str):
    r"""
    Deserialize value back to its original type
    :param value: Value to deserialize
    :param type_str: Type string
    :return: Deserialized value
    :raise ValueError: If unable to convert
    """
    try:
        if type_str == 'bytes':
            return bytes(value)
        if type_str == 'set':
            return set(value)
        if type_str == 'frozenset':
            return frozenset(value)
        if type_str == 'NoneType':
            return None
        if type_str == 'bool':
            return bool(value)
        return {
            'int': int,
            'float': float,
            'str': str,
            'complex': complex,
            'list': list,
            'tuple': tuple,
            'dict': dict,
        }.get(type_str, lambda x: x)(value)
    except Exception:
        raise ValueError(f'Unable to convert value {value} to type {type_str}')
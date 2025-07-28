"""
@file simpsave.py
@author WaterRun
@version 4.0
@date 2025-07-28
@description Source code of simpsave project (YAML version)
"""

import os
import importlib.util
import re
import yaml


def _path_parser(path: str | None) -> str:
    r"""
    Handle and convert paths
    :param path: Path to be processed
    :return: Processed path
    :raise ValueError: If the path is not a string or is invalid
    :raise ImportError: If using :ss: and not installed via pip
    """
    if path is None:
        path = '__ss__.yml'

    if not (isinstance(path, str) and path.endswith('.yml')):
        raise ValueError("Path must be a string and must be a .yml file")

    if path.startswith(':ss:'):
        spec = importlib.util.find_spec("simpsave")
        if spec is None:
            raise ImportError("When using the 'ss' directive, simpsave must be installed via pip")
        simpsave_path = os.path.join(spec.submodule_search_locations[0])
        relative_path = path[len(':ss:'):]
        return os.path.join(simpsave_path, relative_path)

    absolute_path = os.path.abspath(path)

    if not os.path.isfile(absolute_path) and not os.path.isdir(os.path.dirname(absolute_path)):
        raise ValueError(f"Invalid path in the system: {absolute_path}")

    return absolute_path


def _load_yaml(file: str) -> dict:
    r"""
    Load the YAML file
    :param file: Path to the YAML file
    :return: Loaded dict object
    :raise FileNotFoundError: If the file does not exist
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .yml file does not exist: {file}')
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    data = yaml.safe_load(content)
    return data if isinstance(data, dict) else {}


def _dump_yaml(data: dict, file: str) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def write(key: str, value: any, *, file: str | None = None) -> bool:
    r"""
    Write data to the specified .yml file. If the .yml file does not exist, it will be created.
    For lists or dictionaries, every element must also be a Python basic type.
    :param key: Key to write to
    :param value: Value to write
    :param file: Path to the .yml file
    :return: Whether the write was successful
    :raise TypeError: If the value or its elements are not basic types
    :raise FileNotFoundError: If the specified .yml file does not exist
    """

    def _validate_basic_type(value):
        basic_types = (int, float, str, bool, bytes, complex, list, tuple, set, frozenset, dict, type(None))
        if isinstance(value, (list, tuple, set, frozenset)):
            for item in value:
                if not isinstance(item, basic_types):
                    raise TypeError(f"All elements in {type(value).__name__} must be Python basic types.")
                _validate_basic_type(item)
        elif isinstance(value, dict):
            for k, v in value.items():
                if not isinstance(k, basic_types) or not isinstance(v, basic_types):
                    raise TypeError("All keys and values in a dict must be Python basic types.")
                _validate_basic_type(v)
        elif not isinstance(value, basic_types):
            raise TypeError(f"Value must be a Python basic type, got {type(value).__name__} instead.")

    file = _path_parser(file)
    _validate_basic_type(value)

    value_type = type(value).__name__

    if not os.path.exists(file):
        with open(file, 'w', encoding='utf-8') as new_file:
            new_file.write("")

    try:
        data = {}
        if os.path.exists(file) and os.path.getsize(file) > 0:
            try:
                data = _load_yaml(file)
            except Exception:
                data = {}

        if isinstance(value, set):
            value = list(value)
        elif isinstance(value, frozenset):
            value = list(value)
        elif isinstance(value, bytes):
            value = list(value)  # store bytes as list of ints for YAML compatibility

        data[key] = {'value': value, 'type': value_type}

        _dump_yaml(data, file)
        return True
    except Exception:
        return False


def read(key: str, *, file: str | None = None) -> any:
    r"""
    Read data from the specified .yml file for a given key
    :param key: Key to read from
    :param file: Path to the .yml file
    :return: The value after conversion (type casted)
    :raise FileNotFoundError: If the specified .yml file does not exist
    :raise KeyError: If the key does not exist in the file
    :raise ValueError: If the key is illegal
    """
    file = _path_parser(file)
    data = _load_yaml(file)
    if key not in data:
        raise KeyError(f'Key {key} does not exist in file {file}')
    val = data[key]
    value, type_str = val['value'], val['type']
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


def has(key: str, *, file: str | None = None) -> bool:
    r"""
    Check if the specified key exists in the given .yml file.
    :param key: Key to check
    :param file: Path to the .yml file
    :return: True if the key exists, False otherwise
    :raise FileNotFoundError: If the specified .yml file does not exist
    """
    file = _path_parser(file)
    data = _load_yaml(file)
    return key in data


def remove(key: str, *, file: str | None = None) -> bool:
    r"""
    Remove the specified key (entire entry). Returns False if it doesn't exist
    :param key: Key to remove
    :param file: Path to the .yml file
    :return: Whether the removal was successful
    :raise FileNotFoundError: If the specified .yml file does not exist
    """
    file = _path_parser(file)
    data = _load_yaml(file)
    if key not in data:
        return False
    data.pop(key)
    _dump_yaml(data, file)
    return True


def match(regex: str = "", *, file: str | None = None) -> dict[str, any]:
    r"""
    Return key-value pairs that match the regular expression from the .yml file in the format {'key':..,'value':..}
    :param regex: Regular expression string
    :param file: Path to the .yml file
    :return: Dictionary of matched results
    :raise FileNotFoundError: If the specified .yml file does not exist
    """
    file = _path_parser(file)
    data = _load_yaml(file)
    pattern = re.compile(regex)
    result = {}
    for k in data:
        if pattern.match(k):
            result[k] = read(k, file=file)
    return result


def delete(*, file: str | None = None) -> bool:
    r"""
    Delete the entire .yml file. Returns False if it doesn't exist
    :param file: Path to the .yml file to delete
    :return: Whether the deletion was successful
    :raise IOError: If the delete failed
    """
    file = _path_parser(file)
    if not os.path.isfile(file):
        return False
    try:
        os.remove(file)
        return True
    except IOError:
        return False

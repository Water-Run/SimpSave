"""
@file simpsave.py
@author WaterRun
@version 2.3
@date 2025-03-02
@description Source code of simpsave project
"""

import os
import importlib.util
import configparser
import re as regex
import ast


def _path_parser(path: str | None) -> str:
    r"""
    Handle and convert paths
    :param path: Path to be processed
    :return: Processed path
    :raise ValueError: If the path is not a string or is invalid
    :raise ImportError: If using :ss: and not installed via pip
    """
    if path is None:
        path = '__ss__.ini'

    if not (isinstance(path, str) and path.endswith('.ini')):
        raise ValueError("Path must be a string and must be a .ini file")

    if path.startswith(':ss:'):  # Must be installed via pip
        spec = importlib.util.find_spec("simpsave")
        if spec is None:
            raise ImportError("When using the 'ss' directive, simpsave must be installed via pip")

        simpsave_path = os.path.join(spec.submodule_search_locations[0])
        relative_path = path[len(':ss:'):]
        return os.path.join(simpsave_path, relative_path)

    # Convert relative path to absolute path
    absolute_path = os.path.abspath(path)

    # Validate path legality
    if not os.path.isfile(absolute_path) and not os.path.isdir(os.path.dirname(absolute_path)):
        raise ValueError(f"Invalid path in the system: {absolute_path}")

    return absolute_path


def _load_config(file: str) -> configparser.ConfigParser:
    r"""
    Load the configuration file
    :param file: Path to the configuration file
    :return: Loaded ConfigParser object
    :raise FileNotFoundError: If the file does not exist
    """
    config = configparser.ConfigParser(interpolation=None)
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .ini file does not exist: {file}')
    config.read(file)
    return config


def write(key: str, value: any, *, file: str | None = None) -> bool:
    r"""
    Write data to the specified .ini file. If the .ini file does not exist, it will be created
    :param key: Key to write to
    :param value: Value to write
    :param file: Path to the .ini file
    :return: Whether the write was successful
    :raise TypeError: If the value is not a basic type
    :raise FileNotFoundError: If the specified .ini file does not exist
    """
    file = _path_parser(file)
    basic_types = (int, float, str, bool, bytes, complex, list, tuple, set, frozenset, dict, type(None))
    if not isinstance(value, basic_types):
        raise TypeError(f"simpsave only supports Python basic types, i.e. {basic_types}")
    value_type = type(value).__name__

    if not os.path.exists(file):
        with open(file, 'w', encoding='utf-8') as new_file:
            new_file.write("")

    config = configparser.ConfigParser(interpolation=None)
    config.read(file, encoding='utf-8')
    try:
        escaped_value = str(value).encode('unicode-escape').decode('utf-8').replace('\n', '\\n').replace('=', '\\=').replace(':', '\\:')
        config[key] = {'value': str(escaped_value), 'type': value_type}
        with open(file, 'w') as configfile:
            config.write(configfile)
        return True
    except IOError:
        return False


def read(key: str, *, file: str | None = None) -> any:
    r"""
    Read data from the specified .ini file for a given key
    :param key: Key to read from
    :param file: Path to the .ini file
    :return: The value after conversion (type casted)
    :raise FileNotFoundError: If the specified .ini file does not exist
    :raise KeyError: If the key does not exist in the file
    :raise ValueError: If the key is illegal
    """
    file = _path_parser(file)
    config = _load_config(file)
    if key not in config:
        raise KeyError(f'Key {key} does not exist in file {file}')
    value_str = bytes(config[key]['value'].replace('\\n', '\n').replace('\\=', '=').replace('\\:', ':').encode('utf-8')).decode('unicode-escape')
    type_str = config[key]['type']
    try:
        return {
            'int': int,
            'float': float,
            'str': str,
            'bool': lambda x: x == 'True',
            'bytes': bytes,
            'complex': complex,
            'list': ast.literal_eval,
            'tuple': ast.literal_eval,
            'set': ast.literal_eval,
            'frozenset': ast.literal_eval,
            'dict': ast.literal_eval,
            'NoneType': lambda _: None,
        }[type_str](value_str)
    except (KeyError, ValueError):
        raise ValueError(f'Unable to convert value {value_str} to type {type_str}')


def has(key: str, *, file: str | None = None) -> bool:
    r"""
    Check if the specified key exists in the given .ini file.
    :param key: Key to check
    :param file: Path to the .ini file
    :return: True if the key exists, False otherwise
    :raise FileNotFoundError: If the specified .ini file does not exist
    """
    file = _path_parser(file)
    config = _load_config(file)

    return key in config


def remove(key: str, *, file: str | None = None) -> bool:
    r"""
    Remove the specified key (entire section). Returns False if it doesn't exist
    :param key: Key to remove
    :param file: Path to the .ini file
    :return: Whether the removal was successful
    :raise FileNotFoundError: If the specified .ini file does not exist
    """
    file = _path_parser(file)
    config = _load_config(file)
    if key not in config:
        return False
    config.remove_section(key)
    with open(file, 'w') as configfile:
        config.write(configfile)
    return True


def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    r"""
    Return key-value pairs that match the regular expression from the .ini file in the format {'key':..,'value':..}
    :param re: Regular expression string
    :param file: Path to the .ini file
    :return: Dictionary of matched results
    :raise FileNotFoundError: If the specified .ini file does not exist
    """
    file = _path_parser(file)
    config = _load_config(file)
    pattern = regex.compile(re)
    result = {}
    for key in config.sections():
        if pattern.match(key):
            result[key] = read(key, file=file)
    return result


def delete(*, file: str | None = None) -> bool:
    r"""
    Delete the entire .ini file. Returns False if it doesn't exist
    :param file: Path to the .ini file to delete
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
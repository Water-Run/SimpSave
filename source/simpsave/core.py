"""
@file core.py
@author WaterRun
@version 10.0
@date 2025-11-09
@description Source code of simpsave project - Fixed string handling for XML/INI engines
"""

import os
import importlib.util
import re
import json
import xml.etree.ElementTree as ET
from typing import Any


_ENGINE: str = "XML"


def _path_parser(path: str | None, extension: str) -> str:
    r"""
    Handle and convert paths
    :param path: Path to be processed
    :param extension: Expected file extension
    :return: Processed path
    :raise ValueError: If the path is not a string or is invalid
    :raise ImportError: If using :ss: and not installed via pip
    """
    if path is None:
        path = f'__ss__.{extension}'

    if not isinstance(path, str):
        raise ValueError("Path must be a string")

    if not path.endswith(f'.{extension}'):
        raise ValueError(f"Path must be a .{extension} file")

    if path.startswith(':ss:'):
        spec = importlib.util.find_spec("simpsave")
        if spec is None:
            raise ImportError("When using the 'ss' directive, simpsave must be installed via pip")
        simpsave_path = os.path.join(spec.submodule_search_locations[0])
        relative_path = path[len(':ss:'):]
        return os.path.join(simpsave_path, relative_path)

    absolute_path = os.path.abspath(path)
    parent_dir = os.path.dirname(absolute_path)
    
    if parent_dir and not os.path.isdir(parent_dir):
        raise ValueError(f"Invalid path in the system: {absolute_path}")

    return absolute_path


def _validate_basic_type(value: Any) -> None:
    r"""
    Validate that value and its nested elements are basic types
    :param value: Value to validate
    :raise TypeError: If the value or its elements are not basic types
    """
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
            _validate_basic_type(k)
            _validate_basic_type(v)
    elif not isinstance(value, basic_types):
        raise TypeError(f"Value must be a Python basic type, got {type(value).__name__} instead.")


def _python_to_json_compatible(value: Any) -> Any:
    r"""
    Convert Python value to JSON-compatible format
    :param value: Python value
    :return: JSON-compatible value
    """
    if isinstance(value, complex):
        return {'__complex__': True, 'real': value.real, 'imag': value.imag}
    elif isinstance(value, bytes):
        return {'__bytes__': True, 'data': list(value)}
    elif isinstance(value, set):
        return {'__set__': True, 'data': [_python_to_json_compatible(item) for item in value]}
    elif isinstance(value, frozenset):
        return {'__frozenset__': True, 'data': [_python_to_json_compatible(item) for item in value]}
    elif isinstance(value, tuple):
        return {'__tuple__': True, 'data': [_python_to_json_compatible(item) for item in value]}
    elif isinstance(value, list):
        return [_python_to_json_compatible(item) for item in value]
    elif isinstance(value, dict):
        if any(key.startswith('__') and key.endswith('__') for key in value.keys()):
            return {'__dict__': True, 'data': {k: _python_to_json_compatible(v) for k, v in value.items()}}
        return {k: _python_to_json_compatible(v) for k, v in value.items()}
    else:
        return value


def _json_compatible_to_python(value: Any) -> Any:
    r"""
    Convert JSON-compatible value back to Python value
    :param value: JSON-compatible value
    :return: Python value
    """
    if isinstance(value, dict):
        if value.get('__complex__'):
            return complex(value['real'], value['imag'])
        elif value.get('__bytes__'):
            return bytes(value['data'])
        elif value.get('__set__'):
            return set(_json_compatible_to_python(item) for item in value['data'])
        elif value.get('__frozenset__'):
            return frozenset(_json_compatible_to_python(item) for item in value['data'])
        elif value.get('__tuple__'):
            return tuple(_json_compatible_to_python(item) for item in value['data'])
        elif value.get('__dict__'):
            return {k: _json_compatible_to_python(v) for k, v in value['data'].items()}
        else:
            return {k: _json_compatible_to_python(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_json_compatible_to_python(item) for item in value]
    else:
        return value


def _xml_load(file: str) -> dict[str, dict[str, Any]]:
    r"""
    Load XML file
    :param file: Path to the XML file
    :return: Loaded dict object
    :raise FileNotFoundError: If the file does not exist
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .xml file does not exist: {file}')
    
    tree = ET.parse(file)
    root = tree.getroot()
    
    data = {}
    for item in root.findall('item'):
        key = item.get('key')
        value_type = item.find('type').text
        value_str = item.find('value').text or ''
        
        data[key] = {'value': value_str, 'type': value_type}
    
    return data


def _xml_dump(data: dict[str, dict[str, Any]], file: str) -> None:
    r"""
    Dump data to XML file
    :param data: Data to dump
    :param file: Path to the XML file
    """
    root = ET.Element('simpsave')
    
    for key in sorted(data.keys()):
        val = data[key]
        item = ET.SubElement(root, 'item', key=key)
        
        type_elem = ET.SubElement(item, 'type')
        type_elem.text = val['type']
        
        value_elem = ET.SubElement(item, 'value')
        value_elem.text = val['value']
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    tree.write(file, encoding='utf-8', xml_declaration=True)


def _ini_load(file: str) -> dict[str, dict[str, Any]]:
    r"""
    Load INI file
    :param file: Path to the INI file
    :return: Loaded dict object
    :raise FileNotFoundError: If the file does not exist
    :raise RuntimeError: If configparser module is not available
    """
    try:
        import configparser
    except ImportError:
        raise RuntimeError("INI engine requires the 'configparser' module (standard library)")
    
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .ini file does not exist: {file}')
    
    config = configparser.ConfigParser()
    config.read(file, encoding='utf-8')
    
    data = {}
    for section in config.sections():
        value_type = config.get(section, 'type')
        value_str = config.get(section, 'value')
        
        data[section] = {'value': value_str, 'type': value_type}
    
    return data


def _ini_dump(data: dict[str, dict[str, Any]], file: str) -> None:
    r"""
    Dump data to INI file
    :param data: Data to dump
    :param file: Path to the INI file
    :raise RuntimeError: If configparser module is not available
    """
    try:
        import configparser
    except ImportError:
        raise RuntimeError("INI engine requires the 'configparser' module (standard library)")
    
    config = configparser.ConfigParser()
    
    for key in sorted(data.keys()):
        val = data[key]
        config.add_section(key)
        config.set(key, 'type', val['type'])
        config.set(key, 'value', val['value'])
    
    with open(file, 'w', encoding='utf-8') as f:
        config.write(f)


def _json_load(file: str) -> dict[str, dict[str, Any]]:
    r"""
    Load JSON file
    :param file: Path to the JSON file
    :return: Loaded dict object
    :raise FileNotFoundError: If the file does not exist
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .json file does not exist: {file}')
    
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def _json_dump(data: dict[str, dict[str, Any]], file: str) -> None:
    r"""
    Dump data to JSON file
    :param data: Data to dump
    :param file: Path to the JSON file
    """
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _yml_load(file: str) -> dict[str, dict[str, Any]]:
    r"""
    Load YML file
    :param file: Path to the YML file
    :return: Loaded dict object
    :raise FileNotFoundError: If the file does not exist
    :raise RuntimeError: If yaml module is not available
    """
    try:
        import yaml
    except ImportError:
        raise RuntimeError("YML engine requires the 'pyyaml' package. Install with: pip install simpsave[yml]")
    
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .yml file does not exist: {file}')
    
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def _yml_dump(data: dict[str, dict[str, Any]], file: str) -> None:
    r"""
    Dump data to YML file
    :param data: Data to dump
    :param file: Path to the YML file
    :raise RuntimeError: If yaml module is not available
    """
    try:
        import yaml
    except ImportError:
        raise RuntimeError("YML engine requires the 'pyyaml' package. Install with: pip install simpsave[yml]")
    
    with open(file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _toml_load(file: str) -> dict[str, dict[str, Any]]:
    r"""
    Load TOML file
    :param file: Path to the TOML file
    :return: Loaded dict object
    :raise FileNotFoundError: If the file does not exist
    :raise RuntimeError: If tomllib/tomli is not available
    """
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            raise RuntimeError("TOML engine requires 'tomllib' (Python 3.11+) or 'tomli'. Install with: pip install simpsave[toml]")
    
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .toml file does not exist: {file}')
    
    with open(file, 'rb') as f:
        data = tomllib.load(f)
    return data if isinstance(data, dict) else {}


def _toml_dump(data: dict[str, dict[str, Any]], file: str) -> None:
    r"""
    Dump data to TOML file
    :param data: Data to dump
    :param file: Path to the TOML file
    :raise RuntimeError: If tomli_w is not available
    """
    try:
        import tomli_w
    except ImportError:
        raise RuntimeError("TOML write engine requires the 'tomli-w' package. Install with: pip install tomli-w")
    
    with open(file, 'wb') as f:
        tomli_w.dump(data, f)


def _sqlite_connect(file: str):
    r"""
    Connect to SQLite database and ensure table exists
    :param file: Path to the SQLite database file
    :return: Database connection and cursor
    :raise RuntimeError: If sqlite3 module is not available
    """
    try:
        import sqlite3
    except ImportError:
        raise RuntimeError("SQLITE engine requires the 'sqlite3' module (standard library)")
    
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simpsave (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    return conn, cursor


def _sqlite_load(file: str) -> dict[str, dict[str, Any]]:
    r"""
    Load data from SQLite database
    :param file: Path to the SQLite database file
    :return: Loaded dict object
    :raise FileNotFoundError: If the file does not exist
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .db file does not exist: {file}')
    
    conn, cursor = _sqlite_connect(file)
    cursor.execute('SELECT key, value FROM simpsave')
    rows = cursor.fetchall()
    conn.close()
    
    data = {}
    for key, value_blob in rows:
        val = json.loads(value_blob)
        data[key] = val
    return data


def _sqlite_write(key: str, value: Any, value_type: str, file: str) -> None:
    r"""
    Write a key-value pair to SQLite database
    :param key: Key to write
    :param value: Value to write
    :param value_type: Type name of the value
    :param file: Path to the SQLite database file
    """
    json_value = _python_to_json_compatible(value)
    
    conn, cursor = _sqlite_connect(file)
    value_blob = json.dumps({'value': json_value, 'type': value_type}, ensure_ascii=False)
    cursor.execute('INSERT OR REPLACE INTO simpsave (key, value) VALUES (?, ?)', (key, value_blob))
    conn.commit()
    conn.close()


def _sqlite_remove(key: str, file: str) -> bool:
    r"""
    Remove a key from SQLite database
    :param key: Key to remove
    :param file: Path to the SQLite database file
    :return: Whether the removal was successful
    """
    conn, cursor = _sqlite_connect(file)
    cursor.execute('DELETE FROM simpsave WHERE key = ?', (key,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def _redis_connect(host: str, port: int):
    r"""
    Connect to Redis server
    :param host: Redis host
    :param port: Redis port
    :return: Redis connection
    :raise RuntimeError: If redis module is not available
    """
    try:
        import redis
    except ImportError:
        raise RuntimeError("REDIS engine requires the 'redis' package. Install with: pip install simpsave[redis]")
    
    return redis.Redis(host=host, port=port, decode_responses=True)


def _redis_write(key: str, value: Any, value_type: str, host: str = 'localhost', port: int = 6379) -> None:
    r"""
    Write a key-value pair to Redis
    :param key: Key to write
    :param value: Value to write
    :param value_type: Type name of the value
    :param host: Redis host
    :param port: Redis port
    """
    json_value = _python_to_json_compatible(value)
    
    r = _redis_connect(host, port)
    value_blob = json.dumps({'value': json_value, 'type': value_type}, ensure_ascii=False)
    r.set(key, value_blob)


def _redis_read(key: str, host: str = 'localhost', port: int = 6379) -> dict[str, Any]:
    r"""
    Read a key from Redis
    :param key: Key to read
    :param host: Redis host
    :param port: Redis port
    :return: Dictionary with 'value' and 'type' keys
    :raise KeyError: If the key does not exist
    """
    r = _redis_connect(host, port)
    value_blob = r.get(key)
    if value_blob is None:
        raise KeyError(f'Key {key} does not exist in Redis')
    return json.loads(value_blob)


def _redis_has(key: str, host: str = 'localhost', port: int = 6379) -> bool:
    r"""
    Check if a key exists in Redis
    :param key: Key to check
    :param host: Redis host
    :param port: Redis port
    :return: True if the key exists, False otherwise
    """
    r = _redis_connect(host, port)
    return r.exists(key) > 0


def _redis_remove(key: str, host: str = 'localhost', port: int = 6379) -> bool:
    r"""
    Remove a key from Redis
    :param key: Key to remove
    :param host: Redis host
    :param port: Redis port
    :return: Whether the removal was successful
    """
    r = _redis_connect(host, port)
    return r.delete(key) > 0


def _redis_match(regex: str, host: str = 'localhost', port: int = 6379) -> dict[str, Any]:
    r"""
    Match keys in Redis using a regular expression
    :param regex: Regular expression string
    :param host: Redis host
    :param port: Redis port
    :return: Dictionary of matched results
    """
    r = _redis_connect(host, port)
    pattern = re.compile(regex)
    result = {}
    for key in r.scan_iter():
        if pattern.match(key):
            result[key] = read(key, host=host, port=port)
    return result


def engine(name: str = "XML") -> None:
    r"""
    Set the storage engine for SimpSave
    :param name: Engine name (XML, INI, JSON, YML, TOML, SQLITE, REDIS)
    :raise ValueError: If the engine name is invalid
    """
    global _ENGINE
    valid_engines = {"XML", "INI", "JSON", "YML", "TOML", "SQLITE", "REDIS"}
    if name.upper() not in valid_engines:
        raise ValueError(f"Invalid engine name: {name}. Valid options: {valid_engines}")
    _ENGINE = name.upper()


def write(key: str, value: Any, *, file: str | None = None, host: str = 'localhost', port: int = 6379) -> bool:
    r"""
    Write data to the storage backend
    :param key: Key to write to
    :param value: Value to write
    :param file: Path to the storage file (for file-based engines)
    :param host: Redis host (for REDIS engine)
    :param port: Redis port (for REDIS engine)
    :return: Whether the write was successful
    """
    try:
        _validate_basic_type(value)
    except TypeError:
        return False
    
    value_type = type(value).__name__
    
    try:
        if _ENGINE == "REDIS":
            _redis_write(key, value, value_type, host, port)
            return True
        
        if _ENGINE == "SQLITE":
            file = _path_parser(file, 'db')
            _sqlite_write(key, value, value_type, file)
            return True
        
        extensions = {"XML": "xml", "INI": "ini", "JSON": "json", "YML": "yml", "TOML": "toml"}
        ext = extensions[_ENGINE]
        file = _path_parser(file, ext)
        
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as new_file:
                if _ENGINE == "XML":
                    new_file.write('<?xml version="1.0" encoding="utf-8"?>\n<simpsave></simpsave>')
                else:
                    new_file.write("")
        
        load_funcs = {"XML": _xml_load, "INI": _ini_load, "JSON": _json_load, "YML": _yml_load, "TOML": _toml_load}
        dump_funcs = {"XML": _xml_dump, "INI": _ini_dump, "JSON": _json_dump, "YML": _yml_dump, "TOML": _toml_dump}
        
        data = {}
        if os.path.exists(file) and os.path.getsize(file) > 0:
            try:
                data = load_funcs[_ENGINE](file)
            except Exception:
                data = {}
        
        json_value = _python_to_json_compatible(value)
        
        if _ENGINE == "XML" or _ENGINE == "INI":
            data[key] = {
                'value': json.dumps(json_value, ensure_ascii=False, separators=(',', ':')), 
                'type': value_type
            }
        else:
            data[key] = {'value': json_value, 'type': value_type}
        
        dump_funcs[_ENGINE](data, file)
        return True
    except Exception:
        return False


def read(key: str, *, file: str | None = None, host: str = 'localhost', port: int = 6379) -> Any:
    r"""
    Read data from the storage backend
    :param key: Key to read from
    :param file: Path to the storage file (for file-based engines)
    :param host: Redis host (for REDIS engine)
    :param port: Redis port (for REDIS engine)
    :return: The value after conversion
    :raise FileNotFoundError: If the specified file does not exist
    :raise KeyError: If the key does not exist
    :raise ValueError: If unable to convert the value
    """
    if _ENGINE == "REDIS":
        val = _redis_read(key, host, port)
        python_value = _json_compatible_to_python(val['value'])
        return python_value
    elif _ENGINE == "SQLITE":
        file = _path_parser(file, 'db')
        data = _sqlite_load(file)
        if key not in data:
            raise KeyError(f'Key {key} does not exist in file {file}')
        val = data[key]
        python_value = _json_compatible_to_python(val['value'])
        return python_value
    else:
        extensions = {"XML": "xml", "INI": "ini", "JSON": "json", "YML": "yml", "TOML": "toml"}
        ext = extensions[_ENGINE]
        file = _path_parser(file, ext)
        
        load_funcs = {"XML": _xml_load, "INI": _ini_load, "JSON": _json_load, "YML": _yml_load, "TOML": _toml_load}
        data = load_funcs[_ENGINE](file)
        
        if key not in data:
            raise KeyError(f'Key {key} does not exist in file {file}')
        val = data[key]
    
    value, type_str = val['value'], val['type']
    
    if _ENGINE == "XML" or _ENGINE == "INI":
        try:
            json_value = json.loads(value)
            python_value = _json_compatible_to_python(json_value)
            return python_value
        except Exception as e:
            raise ValueError(f'Unable to convert value to type {type_str}: {e}')
    
    try:
        python_value = _json_compatible_to_python(value)
        return python_value
    except Exception as e:
        raise ValueError(f'Unable to convert value to type {type_str}: {e}')


def has(key: str, *, file: str | None = None, host: str = 'localhost', port: int = 6379) -> bool:
    r"""
    Check if a key exists in the storage backend
    :param key: Key to check
    :param file: Path to the storage file (for file-based engines)
    :param host: Redis host (for REDIS engine)
    :param port: Redis port (for REDIS engine)
    :return: True if the key exists, False otherwise
    :raise FileNotFoundError: If the specified file does not exist
    """
    if _ENGINE == "REDIS":
        return _redis_has(key, host, port)
    
    if _ENGINE == "SQLITE":
        file = _path_parser(file, 'db')
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .db file does not exist: {file}')
        data = _sqlite_load(file)
        return key in data
    
    extensions = {"XML": "xml", "INI": "ini", "JSON": "json", "YML": "yml", "TOML": "toml"}
    ext = extensions[_ENGINE]
    file = _path_parser(file, ext)
    
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .{ext} file does not exist: {file}')
    
    load_funcs = {"XML": _xml_load, "INI": _ini_load, "JSON": _json_load, "YML": _yml_load, "TOML": _toml_load}
    data = load_funcs[_ENGINE](file)
    
    return key in data


def remove(key: str, *, file: str | None = None, host: str = 'localhost', port: int = 6379) -> bool:
    r"""
    Remove a key from the storage backend
    :param key: Key to remove
    :param file: Path to the storage file (for file-based engines)
    :param host: Redis host (for REDIS engine)
    :param port: Redis port (for REDIS engine)
    :return: Whether the removal was successful
    :raise FileNotFoundError: If the specified file does not exist
    """
    if _ENGINE == "REDIS":
        return _redis_remove(key, host, port)
    
    if _ENGINE == "SQLITE":
        file = _path_parser(file, 'db')
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .db file does not exist: {file}')
        return _sqlite_remove(key, file)
    
    extensions = {"XML": "xml", "INI": "ini", "JSON": "json", "YML": "yml", "TOML": "toml"}
    ext = extensions[_ENGINE]
    file = _path_parser(file, ext)
    
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .{ext} file does not exist: {file}')
    
    load_funcs = {"XML": _xml_load, "INI": _ini_load, "JSON": _json_load, "YML": _yml_load, "TOML": _toml_load}
    dump_funcs = {"XML": _xml_dump, "INI": _ini_dump, "JSON": _json_dump, "YML": _yml_dump, "TOML": _toml_dump}
    
    data = load_funcs[_ENGINE](file)
    
    if key not in data:
        return False
    
    data.pop(key)
    dump_funcs[_ENGINE](data, file)
    return True


def match(regex: str = "", *, file: str | None = None, host: str = 'localhost', port: int = 6379) -> dict[str, Any]:
    r"""
    Return key-value pairs that match the regular expression
    :param regex: Regular expression string
    :param file: Path to the storage file (for file-based engines)
    :param host: Redis host (for REDIS engine)
    :param port: Redis port (for REDIS engine)
    :return: Dictionary of matched results
    :raise FileNotFoundError: If the specified file does not exist
    """
    if _ENGINE == "REDIS":
        return _redis_match(regex, host, port)
    
    if _ENGINE == "SQLITE":
        file = _path_parser(file, 'db')
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .db file does not exist: {file}')
        data = _sqlite_load(file)
    else:
        extensions = {"XML": "xml", "INI": "ini", "JSON": "json", "YML": "yml", "TOML": "toml"}
        ext = extensions[_ENGINE]
        file = _path_parser(file, ext)
        
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .{ext} file does not exist: {file}')
        
        load_funcs = {"XML": _xml_load, "INI": _ini_load, "JSON": _json_load, "YML": _yml_load, "TOML": _toml_load}
        data = load_funcs[_ENGINE](file)
    
    pattern = re.compile(regex)
    result = {}
    for k in data:
        if pattern.match(k):
            result[k] = read(k, file=file)
    return result


def delete(*, file: str | None = None) -> bool:
    r"""
    Delete the storage file
    :param file: Path to the storage file to delete
    :return: Whether the deletion was successful
    """
    if _ENGINE == "REDIS":
        return False
    
    extensions = {"XML": "xml", "INI": "ini", "JSON": "json", "YML": "yml", "TOML": "toml", "SQLITE": "db"}
    ext = extensions[_ENGINE]
    
    try:
        file = _path_parser(file, ext)
    except ValueError:
        return False
    
    if not os.path.isfile(file):
        return False
    
    try:
        os.remove(file)
        return True
    except (IOError, OSError):
        return False
"""
@file core.py
@author WaterRun
@version 10
@date 2025-11-07
@description Core API for SimpSave
"""

from typing import Any, Optional
from pathlib import Path
from .engines import get_engine, list_available_engines
from .utils import parse_path


# 文件后缀到引擎的映射
EXTENSION_MAP = {
    '.simpsave': 'FILE',
    '.ini': 'INI',
    '.yml': 'YML',
    '.yaml': 'YML',
    '.toml': 'TOML',
    '.json': 'JSON',
    '.xml': 'XML',
    '.db': 'SQLITE',
    '.sqlite': 'SQLITE',
}


def _get_engine_for_file(file: Optional[str]) -> tuple:
    r"""
    Choose the appropriate engine based on the file path or connection string
    :param file: File path
    :return: (Engine instance, Resolved file path)
    """

    if file and file.startswith('redis://'):
        engine_class = get_engine('REDIS')
        return engine_class(), file
    
    default_engine = get_engine('FILE') if 'FILE' in list_available_engines() else get_engine('YML')
    default_suffix = default_engine.get_default_suffix()
    
    resolved_file = parse_path(file, default_suffix)
    
    suffix = Path(resolved_file).suffix.lower()
    engine_name = EXTENSION_MAP.get(suffix, 'FILE')
    
    try:
        engine_class = get_engine(engine_name)
        return engine_class(), resolved_file
    except Exception as e:
        print(f"Warning: {e}")
        print(f"Falling back to default engine...")
        return default_engine(), resolved_file.replace(suffix, default_suffix)


def write(key: str, value: Any, *, file: Optional[str] = None) -> bool:
    r"""
    Write data to the specified storage. If the storage does not exist, it will be created.
    For lists or dictionaries, every element must also be a Python basic type.
    :param key: Key to write to
    :param value: Value to write
    :param file: Path to the storage or connection string
    :return: Whether the write was successful
    :raise TypeError: If the value or its elements are not basic types
    :raise FileNotFoundError: If the specified storage does not exist
    """
    engine, resolved_file = _get_engine_for_file(file)
    return engine.write(key, value, resolved_file)


def read(key: str, *, file: Optional[str] = None) -> Any:
    r"""
    Read data from the specified storage for a given key
    :param key: Key to read from
    :param file: Path to the storage or connection string
    :return: The value after conversion (type casted)
    :raise FileNotFoundError: If the specified storage does not exist
    :raise KeyError: If the key does not exist in the storage
    :raise ValueError: If the key is illegal
    """
    engine, resolved_file = _get_engine_for_file(file)
    return engine.read(key, resolved_file)


def has(key: str, *, file: Optional[str] = None) -> bool:
    r"""
    Check if the specified key exists in the given storage.
    :param key: Key to check
    :param file: Path to the storage or connection string
    :return: True if the key exists, False otherwise
    :raise FileNotFoundError: If the specified storage does not exist
    """
    engine, resolved_file = _get_engine_for_file(file)
    return engine.has(key, resolved_file)


def remove(key: str, *, file: Optional[str] = None) -> bool:
    r"""
    Remove the specified key (entire entry). Returns False if it doesn't exist
    :param key: Key to remove
    :param file: Path to the storage or connection string
    :return: Whether the removal was successful
    :raise FileNotFoundError: If the specified storage does not exist
    """
    engine, resolved_file = _get_engine_for_file(file)
    return engine.remove(key, resolved_file)


def match(regex: str = "", *, file: Optional[str] = None) -> dict[str, Any]:
    r"""
    Return key-value pairs that match the regular expression from the storage in the format {'key':..,'value':..}
    :param regex: Regular expression string
    :param file: Path to the storage or connection string
    :return: Dictionary of matched results
    :raise FileNotFoundError: If the specified storage does not exist
    """
    engine, resolved_file = _get_engine_for_file(file)
    return engine.match(regex, resolved_file)


def delete(*, file: Optional[str] = None) -> bool:
    r"""
    Delete the entire storage. Returns False if it doesn't exist
    :param file: Path to the storage or connection string to delete
    :return: Whether the deletion was successful
    :raise IOError: If the delete failed
    """
    engine, resolved_file = _get_engine_for_file(file)
    return engine.delete(resolved_file)
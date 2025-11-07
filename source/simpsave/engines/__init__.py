"""
@file __init__.py
@author WaterRun
@version 10
@date 2025-11-07
@description Engine registry and management for SimpSave
"""

from typing import Dict, Type
from .base import BaseEngine
from ..exceptions import EngineNotAvailableError


r"""Engine Registry"""
_engines: Dict[str, Type[BaseEngine]] = {}
_engine_classes = {}  


def register_engine(name: str, engine_class: Type[BaseEngine]) -> None:
    r"""
    Register engine
    :param name: Engine name
    :param engine_class: Engine class  
    """
    _engine_classes[name.upper()] = engine_class
    if engine_class.check_available():
        _engines[name.upper()] = engine_class


def get_engine(name: str) -> Type[BaseEngine]:
    r"""
    Get engine
    :param name: Engine name
    :return: Engine class
    :raise EngineNotAvailableError: If engine is not available
    """
    name = name.upper()
    
    if name not in _engines:
        if name in _engine_classes:
            raise EngineNotAvailableError(
                f"Engine '{name}' is not available. Required dependencies are not installed.\n"
                f"Install with: pip install simpsave[{name.lower()}]\n"
                f"Available engines: {list(_engines.keys())}"
            )
        else:
            raise EngineNotAvailableError(
                f"Unknown engine '{name}'.\n"
                f"Available engines: {list(_engines.keys())}"
            )
    
    return _engines[name]


def list_available_engines() -> list:
    r"""
    List available engines
    :return: List of available engine names
    """
    return list(_engines.keys())


def list_all_engines() -> dict:
    r"""
    List all engines and their availability
    :return: Mapping of engine names to their availability
    """
    return {name: name in _engines for name in _engine_classes.keys()}


def _auto_register() -> None:
    r"""
    Automatically register all engines
    """
    try:
        from .simp import SimpEngine
        register_engine('SIMP', SimpEngine)
    except ImportError:
        ...
    
    try:
        from .yml import YmlEngine
        register_engine('YML', YmlEngine)
    except ImportError:
        ...
    
    try:
        from .ini import IniEngine
        register_engine('INI', IniEngine)
    except ImportError:
        ...
        
    try:
        from .xml import XmlEngine  # 添加这里
        register_engine('XML', XmlEngine)
    except ImportError:
        ...
    
    try:
        from .json import JsonEngine
        register_engine('JSON', JsonEngine)
    except ImportError:
        ...
    
    try:
        from .toml import TomlEngine
        register_engine('TOML', TomlEngine)
    except ImportError:
        ...
    
    try:
        from .sqlite import SqliteEngine
        register_engine('SQLITE', SqliteEngine)
    except ImportError:
        ...
    
    try:
        from .redis import RedisEngine
        register_engine('REDIS', RedisEngine)
    except ImportError:
        ...


_auto_register()
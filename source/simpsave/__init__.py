"""
@file __init__.py
@author WaterRun
@version 10
@date 2025-11-07
@description SimpSave: Easy Python Basic Variable Persistence Library
"""

from .core import write, read, has, remove, match, delete
from .engines import list_available_engines, list_all_engines
from .exceptions import SimpSaveError, EngineNotAvailableError, InvalidPathError, InvalidValueError

from .engines.json import JsonEngine
from .engines.redis import RedisEngine
from .engines.simp import SimpEngine
from .engines.yml import YmlEngine
from .engines.ini import IniEngine
from .engines.toml import TomlEngine
from .engines.sqlite import SqliteEngine
from .engines.xml import XmlEngine

__version__ = '10.0.0'
__all__ = [
    'write',
    'read',
    'has',
    'remove',
    'match',
    'delete',
    'list_available_engines',
    'list_all_engines',
    'SimpSaveError',
    'EngineNotAvailableError',
    'InvalidPathError',
    'InvalidValueError',
    'JsonEngine',
    'RedisEngine',
    'SimpEngine',
    'XmlEngine',
    'YmlEngine',
    'IniEngine',
    'TomlEngine',
    'SqliteEngine',
]
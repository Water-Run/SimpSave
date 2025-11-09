"""
@file __init__.py
@author WaterRun
@version 10.0
@date 2025-11-09
@description SimpSave package initialization
"""

from .simpsave import (
    engine,
    write,
    read,
    has,
    remove,
    match,
    delete,
)

__version__ = "10.0.0"
__author__ = "WaterRun"
__all__ = [
    "engine",
    "write",
    "read",
    "has",
    "remove",
    "match",
    "delete",
]
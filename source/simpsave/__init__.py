"""
@file __init__.py
@author WaterRun
@version 10.1
@date 2025-11-10
@description SimpSave package initialization
"""

from .core import (
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
    "write",
    "read",
    "has",
    "remove",
    "match",
    "delete",
]
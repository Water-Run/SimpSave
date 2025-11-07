"""
@file exceptions.py
@author WaterRun
@version 10
@date 2025-11-07
@description Exception definitions for SimpSave
"""


class SimpSaveError(Exception):
    ...


class EngineNotAvailableError(SimpSaveError):
    ...


class InvalidPathError(SimpSaveError):
    ...


class InvalidValueError(SimpSaveError):
    ...

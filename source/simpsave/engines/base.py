"""
@file base.py
@author WaterRun
@version 10
@date 2025-11-07
@description Base engine class for SimpSave
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseEngine(ABC):
    r"""
    Base Engine Class
    """

    @abstractmethod
    def write(self, key: str, value: Any, file: str) -> bool:
        r"""
        Write data to the storage
        :param key: Key to write to
        :param value: Value to write
        :param file: Storage location
        :return: Whether the write was successful
        """
        ...

    @abstractmethod
    def read(self, key: str, file: str) -> Any:
        r"""
        Read data from the storage
        :param key: Key to read from
        :param file: Storage location
        :return: The value after conversion
        :raise KeyError: If the key does not exist
        """
        ...

    @abstractmethod
    def has(self, key: str, file: str) -> bool:
        r"""
        Check if the specified key exists
        :param key: Key to check
        :param file: Storage location
        :return: True if the key exists, False otherwise
        """
        ...

    @abstractmethod
    def remove(self, key: str, file: str) -> bool:
        r"""
        Remove the specified key
        :param key: Key to remove
        :param file: Storage location
        :return: Whether the removal was successful
        """
        ...

    @abstractmethod
    def match(self, regex: str, file: str) -> dict:
        r"""
        Return key-value pairs that match the regular expression
        :param regex: Regular expression string
        :param file: Storage location
        :return: Dictionary of matched results
        """
        ...

    @abstractmethod
    def delete(self, file: str) -> bool:
        r"""
        Delete the entire storage
        :param file: Storage location
        :return: Whether the deletion was successful
        """
        ...

    @classmethod
    @abstractmethod
    def check_available(cls) -> bool:
        r"""
        Check if the engine is available (dependencies installed)
        :return: True if available, False otherwise
        """
        ...

    @classmethod
    @abstractmethod
    def get_default_suffix(cls) -> str:
        r"""
        Get the default file suffix for this engine
        :return: File suffix (e.g., '.yml')
        """
        ...
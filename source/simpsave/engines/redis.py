"""
@file redis.py
@author WaterRun
@version 10
@date 2025-11-07
@description REDIS engine for SimpSave
"""

import re
import math
from .base import BaseEngine
from ..utils import validate_basic_type, serialize_value, deserialize_value


class RedisEngine(BaseEngine):
    r"""
    REDIS Engine
    """

    @classmethod
    def check_available(cls) -> bool:
        try:
            import redis
            return True
        except ImportError:
            return False

    @classmethod
    def get_default_suffix(cls) -> str:
        return ''  # Redis doesn't use files

    def _get_client(self, connection_str: str):
        r"""
        Get Redis client from connection string
        :param connection_str: Redis connection string (e.g., 'redis://localhost:6379/0')
        :return: Redis client
        """
        import redis
        return redis.from_url(connection_str)

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__

        try:
            value = serialize_value(value)
            value_str = repr(value)
            
            client = self._get_client(file)
            
            # Store as hash with value and type
            client.hset(f"ss:{key}", mapping={
                'value': value_str,
                'type': value_type
            })
            
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        client = self._get_client(file)
        
        data = client.hgetall(f"ss:{key}")
        
        if not data:
            raise KeyError(f'Key {key} does not exist in Redis')
        
        value_str = data[b'value'].decode('utf-8')
        type_str = data[b'type'].decode('utf-8')
        
        # Fix: Provide math.inf and math.nan in eval namespace
        value = eval(value_str, {"__builtins__": {}, "inf": math.inf, "nan": math.nan})
        return deserialize_value(value, type_str)

    def has(self, key: str, file: str) -> bool:
        try:
            client = self._get_client(file)
            return client.exists(f"ss:{key}") > 0
        except Exception:
            return False

    def remove(self, key: str, file: str) -> bool:
        try:
            client = self._get_client(file)
            result = client.delete(f"ss:{key}")
            return result > 0
        except Exception:
            return False

    def match(self, regex: str, file: str) -> dict:
        try:
            client = self._get_client(file)
            
            keys = client.keys("ss:*")
            
            pattern = re.compile(regex)
            result = {}
            
            for redis_key in keys:
                key = redis_key.decode('utf-8')[3:]  # Remove 'ss:' prefix
                if pattern.search(key): 
                    result[key] = self.read(key, file)
            
            return result
        except Exception:
            return {}

    def delete(self, file: str) -> bool:
        r"""
        Delete all SimpSave keys from Redis
        :param file: Redis connection string
        :return: Whether the deletion was successful
        """
        try:
            client = self._get_client(file)
            keys = client.keys("ss:*")
            if keys:
                client.delete(*keys)
            return True
        except Exception:
            return False
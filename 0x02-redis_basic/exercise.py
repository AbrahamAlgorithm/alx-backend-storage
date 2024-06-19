#!/usr/bin/env python3
"""
Cache module for storing data in Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for storing data in Redis.

    The Cache class provides methods to store data in a Redis database
    using a randomly generated key.
    """

    def __init__(self):
        """
        Initialize the Cache instance.

        This method initializes a Redis client instance and flushes the
        database to ensure a clean state.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


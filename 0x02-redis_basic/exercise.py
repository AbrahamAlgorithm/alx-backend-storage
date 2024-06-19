#!/usr/bin/env python3
"""
Cache module for storing data in Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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


    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the given key and an optional
        conversion function.

        Args:
            key (str): The key to retrieve the data from Redis.
            fn (Optional[Callable]): A callable function to convert the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, possibly
            converted using the provided function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a string from Redis using the given key.

        Args:
            key (str): The key to retrieve the string from Redis.

        Returns:
            Union[str, None]: The retrieved string, or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer from Redis using the given key.

        Args:
            key (str): The key to retrieve the integer from Redis.

        Returns:
            Union[int, None]: The retrieved integer, or None if the key does not exist.
        """
        return self.get(key, lambda d: int(d))


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

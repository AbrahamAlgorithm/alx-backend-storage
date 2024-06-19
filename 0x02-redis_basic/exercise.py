#!/usr/bin/env python3
"""
Cache module for storing and retrieving data in Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be wrapped by the decorator.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count the number of calls to the method.

        Args:
            self: The instance of the class.
            *args: The positional arguments of the method.
            **kwargs: The keyword arguments of the method.

        Returns:
            The return value of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cache class for storing and retrieving data in Redis.

    The Cache class provides methods to store data in a Redis database
    using a randomly generated key, and retrieve data with optional
    conversion functions.
    """

    def __init__(self):
        """
        Initialize the Cache instance.

        This method initializes a Redis client instance and flushes the
        database to ensure a clean state.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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

    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))


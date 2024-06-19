#!/usr/bin/env python3
"""
Cache module for storing and retrieving data in Redis.
"""

import redis
import uuid
from typing import Callable


def call_history(method: Callable) -> Callable:
    """
    Decorator that logs the input parameters and output values of a method into Redis lists.

    Args:
        method (Callable): The method to be wrapped by the decorator.

    Returns:
        Callable: The wrapped method with logging functionality.
    """
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to log input parameters and output values into Redis lists.

        Args:
            self: The instance of the class.
            *args: The positional arguments of the method.
            **kwargs: The keyword arguments of the method.

        Returns:
            The return value of the original method.
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        # Log input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the original method
        result = method(self, *args, **kwargs)

        # Log output value
        self._redis.rpush(output_key, result)

        return result

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

    @call_history
    def store(self, data: str) -> str:
        """
        Store data in Redis using a randomly generated key.

        Args:
            data (str): The data to store in Redis.

        Returns:
            str: The generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str) -> str:
        """
        Retrieve data from Redis using the given key.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            str: The retrieved data.
        """
        return self._redis.get(key)

    def get_list(self, key: str) -> list:
        """
        Retrieve a list from Redis using the given key.

        Args:
            key (str): The key to retrieve the list from Redis.

        Returns:
            list: The retrieved list.
        """
        return self._redis.lrange(key, 0, -1)


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache.get_list("{}:inputs".format(cache.store.__qualname__))
    outputs = cache.get_list("{}:outputs".format(cache.store.__qualname__))

    print("inputs:", inputs)
    print("outputs:", outputs)


#!/usr/bin/env python3
"""Using redis to create a cache"""


import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """The function call history"""
    key = method.__qualname__
    key_inp = key + ":inputs"
    key_out = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''The wrapper method'''
        self._redis.rpush(key_inp, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(key_out, result)
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    '''Decorator for counting'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''The wrapper method'''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable) -> Callable:
    '''replay the history of a particular func'''
    m_key = method.__qualname__
    inputs = m_key + ":inputs"
    outputs = m_key + ":outputs"
    redis = method.__self__._redis
    cnt = redis.get(m_key).decode("utf-8")
    print("{} was called {} times:".format(m_key, cnt))
    AllInp = redis.lrange(inputs, 0, -1)
    AllOut = redis.lrange(outputs, 0, -1)
    allData = list(zip(AllInp, AllOut))
    for k, v in allData:
        key = k.decode("utf-8")
        value = v.decode("utf-8")
        print("{}(*{}) -> {}".format(m_key, key, value))


class Cache:
    """This is a Cache using redis
    """

    def __init__(self) -> None:
        """Intialization for cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """A store method"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[bytes, str, float, int, None]:
        """get original element"""
        val = self._redis.get(key)
        if fn:
            return fn(val)
        return val

    def get_str(self, data: str) -> str:
        """Decode the redis value"""
        return data.decode("utf-8")

    def get_int(self, data: str) -> int:
        """return the integer"""
        return int(data)

#!/usr/bin/env python3
"""This module has a class Cache"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """This class has a constructor and a store method"""
    def __init__(self):
        """
        store an instance of the Redis client as a private variable
        named _redis (using redis.Redis()) and
        flush the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        self.id = str(uuid.uuid4())
        self._redis.set(self.id, data)
        return self.id

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        take a key string argument and
        an optional Callable argument named fn.
        This callable will be used to
        convert the data back to the desired format.
        Remember to conserve the original Redis.get behavior
        if the key does not exist.
        """
        res = self._redis.get(key)
        if fn is not None:
            return fn(res)
        return res

    def get_int(self, key: str) -> Union[int, None]:
        """
        returns the value stored in the redis store
        at the key as an int
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Union[str, None]:
        """
        returns the value stored in the reds store
        at the key as str
        """
        return self.get(key, str)

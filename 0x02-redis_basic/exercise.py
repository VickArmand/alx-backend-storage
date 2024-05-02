#!/usr/bin/env python3
"""This module has a class Cache"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def call_history(method: Callable) -> Callable:
    """
    decorates a method to record its input output history
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        meth_name = method.__qualname__
        self._redis.rpush(meth_name + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(meth_name + ":outputs", output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    displays the history of calls made by a particular method by retrieving
    the inputs and outputs saved on the redis store
    """
    meth_name = method.__qualname__
    redis_db = method.__self__._redis
    inputs = redis_db.lrange(meth_name + ":inputs", 0, -1)
    outputs = redis_db.lrange(meth_name + ":outputs", 0, -1)

    print(f"{meth_name} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        input = input.decode("utf-8")
        output = output.decode("utf-8")
        print(f"{meth_name}(*{input}) -> {output}")


def count_calls(method: Callable) -> Callable:
    """
    decorates a method to count how many times it was called
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


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
            fn: Optional[Callable] = None) -> Union[str,
                                                    bytes,
                                                    int,
                                                    float,
                                                    None]:
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

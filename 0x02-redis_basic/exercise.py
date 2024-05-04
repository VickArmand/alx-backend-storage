#!/usr/bin/env python3
"""This module has a class Cache"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def replay(method):
    """
    function to display the history of calls
    of a particular function.
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


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs
    and outputs for a particular function.
    Everytime the original function will be called,
    we will add its input parameters to one list in redis,
    and store its output into another list.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        use the decorated function’s qualified name and append
        ":inputs" and ":outputs" to create input and output list keys,
        respectively.
        call_history has a single parameter named method
        that is a Callable and returns a Callable.
        In the new function that the decorator will return,
        use rpush to append the input arguments.
        Remember that Redis can only store strings, bytes and numbers.
        Therefore, we can simply use str(args) to normalize.
        We can ignore potential kwargs for now.
        Execute the wrapped function to retrieve the output.
        Store the output using rpush in the "...:outputs" list,
        then return the output.
        Decorate Cache.store with call_history.
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    takes a single method Callable argument and
    returns a Callable
    As a key, use the qualified name of method
    using the __qualname__ dunder method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
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

    @call_history
    @count_calls
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
            fn: Optional[Callable] = None) -> Union[
                str,
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

#!/usr/bin/env python3
"""
The core of the function is very simple.
It uses the requests module to obtain the HTML content
of a particular URL and returns it.
"""
import redis
import requests as re
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    track how many times a particular URL was accessed in the key "count:{url}"
    and cache the result with an expiration time of 10 seconds.
    Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response
    and test your caching.
    Bonus: implement this use case with decorators.
    """
    return re.get(url).text

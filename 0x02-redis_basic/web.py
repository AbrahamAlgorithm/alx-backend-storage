#!/usr/bin/env python3
"""
Module for fetching web pages and caching results using Redis, implemented with decorators.
"""

import requests
import redis
import time
from functools import wraps

# Initialize Redis connection
redis_conn = redis.Redis()

def cache_with_redis(expires=10):
    """
    Decorator that caches the result of a function in Redis with a specified expiration time.

    Args:
        expires (int): Expiration time in seconds for Redis cache. Default is 10 seconds.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            # Check Redis cache first
            cached_html = redis_conn.get(url)
            if cached_html:
                print(f"Cache hit for {url}")
                return cached_html.decode('utf-8')

            # If not cached, fetch from the URL
            html_content = func(url)

            # Cache the result in Redis with expiration time
            redis_conn.setex(url, expires, html_content)

            return html_content
        return wrapper
    return decorator

def track_access_count(func):
    """
    Decorator that tracks the number of times a function is called for each URL.
    """
    @wraps(func)
    def wrapper(url):
        # Track the number of accesses for this URL
        redis_conn.incr(f"count:{url}")
        return func(url)
    return wrapper

@cache_with_redis()
@track_access_count
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a web page from the given URL.

    Args:
        url (str): The URL of the web page.

    Returns:
        str: The HTML content of the web page.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    print(get_page(url))


#!/usr/bin/env python3
"""requesting to the web"""


import redis
import requests
r = redis.Redis()
count = 0


def get_page(url: str) -> str:
    '''Get the content of a page'''
    r.set(f"cached:{url}", count)
    response = requests.get(url)
    r.incr(f"count:{url}")
    r.setex(f"cached:{url}", 10,
            r.get(f"cached:{url}"))
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')

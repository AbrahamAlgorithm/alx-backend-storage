#!/usr/bin/env python3
"""
Module for fetching web pages, caching results, and tracking access counts using Redis.
"""

import redis
import requests

# Initialize Redis connection
redis_conn = redis.Redis()

def get_page(url: str) -> str:
    """
    Fetches the HTML content of a web page from the given URL,
    caches the response in Redis with a TTL of 10 seconds,
    and tracks the number of accesses for the URL.

    Args:
        url (str): The URL of the web page.

    Returns:
        str: The HTML content of the web page.
    """
    try:
        # Attempt to fetch the cached content from Redis
        cached_content = redis_conn.get(f"cached:{url}")
        if cached_content:
            print(f"Cache hit for {url}")
            return cached_content.decode('utf-8')

        # If not cached, fetch from the URL
        response = requests.get(url)
        html_content = response.text

        # Cache the response in Redis with a TTL of 10 seconds
        redis_conn.setex(f"cached:{url}", 10, html_content)

        # Track the number of accesses for this URL
        redis_conn.incr(f"count:{url}")

        return html_content

    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    print(get_page(url))


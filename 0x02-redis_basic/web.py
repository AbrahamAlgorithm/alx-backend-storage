#!/usr/bin/env python3
"""
Module for fetching and caching web pages.
"""

import requests
import redis

# Initialize Redis connection
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL and caches the result using Redis.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the web page.
    """
    # Check Redis cache first
    cached_html = redis_client.get(url)
    if cached_html:
        return cached_html.decode('utf-8')

    # If not cached, fetch from the web
    response = requests.get(url)
    html_content = response.text

    # Cache the result with a 10-second expiration
    redis_client.setex(url, 10, html_content)

    # Track the number of accesses to this URL
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    return html_content


if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    html = get_page(url)
    print(html)


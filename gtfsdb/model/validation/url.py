from urllib.parse import urlparse


def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.hostname)

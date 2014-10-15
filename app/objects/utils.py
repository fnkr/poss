# Python Utils
import re

# Pygments
from pygments.lexers import get_lexer_for_filename


def human_readable_size(num):
    if not num:
        return ''

    for x in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.2f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def pygments_supports(filename):
    try:
        get_lexer_for_filename(filename)
        return True
    except Exception:
        return False


is_valid_ur_regex = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
def is_valid_url(url):
    return url is not None and is_valid_ur_regex.search(url)


def format_object_title(title):
    return ' '.join(title\
              .replace('>', ' » ')\
              .replace('/', ' » ')\
              .replace('»', ' » ')\
              .split())

# Python Utils
import datetime
import itertools
import os.path
from datetime import timedelta

# PyGeoIP
import pygeoip


def ip(request):
    try:
        request.headers['X-Forwarded-For'].split(',')[0]
    except KeyError:
        return request.remote_addr
    else:
        return request.headers['X-Forwarded-For'].split(',')[0]


def referrer(request):
    try:
        return request.referrer
    except Exception:
        return None


try:
    gi = pygeoip.GeoIP(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../GeoIP.dat'), pygeoip.MEMORY_CACHE)
except Exception:
    gi = None

try:
    gi6 = pygeoip.GeoIP(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../GeoIPv6.dat'), pygeoip.MEMORY_CACHE)
except Exception:
    gi6 = None


def country_code(ip):
    if gi:
        try:
            ip.index('.')
            return gi.country_code_by_addr(ip)
        except Exception:
            pass

    if gi6:
        try:
            ip.index(':')
            return gi6.country_code_by_addr(ip)
        except Exception:
            pass

    return None


def find_monday(d):
    days_ahead = d.weekday()
    return d - timedelta(days_ahead)


SCOPE_NAME_TO_DAYS = {
    'y': 365,
    'm': 30,
    'w': 7,
    'd': 1,
}


def make_daterange(start, stop, scope):
    scope_days = SCOPE_NAME_TO_DAYS[scope]

    for i in itertools.count():
        x = get_first_day(start + timedelta(i * scope_days), scope)
        if x > stop:
            break
        yield x


def get_first_day(dt, scope):
    if scope == 'y':
        return datetime.datetime(dt.year, 1, 1)
    elif scope == 'm':
        return datetime.datetime(dt.year, dt.month, 1)
    elif scope == 'w':
        return find_monday(dt)
    elif scope == 'd':
        return datetime.datetime(dt.year, dt.month, dt.day)

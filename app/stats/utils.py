# Python Utils
import os.path
from datetime import datetime, date, timedelta

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


def missing_duplicated_dates_helper(strings, dateformat, start):
    if len(strings) == 0:
        return strings

    # format strings to dates
    dates = [datetime.strptime(string, dateformat) for string in strings]
    dates.append(start)
    dates.sort()

    # find missing dates and append them
    [dates.append(date) for date in set(dates[0]+timedelta(x) for x in range((dates[-1]-dates[0]).days))]

    # format dates back to strings
    strings = [datetime.strftime(date, dateformat) for date in dates]

    # remove duplicates
    strings = list(set(strings))

    # sort
    strings.sort()

    return strings

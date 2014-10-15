# Python Utils
import os.path

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

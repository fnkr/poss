# Python Utils
from urllib.parse import urlparse
import re

# Flask
from flask import abort
from flask import current_app
from flask import redirect
from flask import url_for


def is_internal(request, allowed=None):
    try:
        referrer = urlparse(request.referrer)
        if referrer.netloc == current_app.config['SERVER_NAME']:
            if allowed:
                for path in allowed:
                    if referrer.path == path:
                        return True
                return False
            else:
                return True
        else:
            return False
    except Exception:
        return False


def valid_email(email):
    return True if re.match(r'[^@]+@[^@]+\.[^@]+', email) else False


def auth_error_return_helper(s):
    if s.auth_error_nouser():
        return redirect(url_for('auth.login'))
    else:
        return abort(403)

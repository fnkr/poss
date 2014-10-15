# SQLAlchemy
from app import db

# POSS Models
from .models import User
from .models import ApiKey


class AuthError():
    auth_error = True

    def __init__(self, reason, auth_method):
        self.auth_method = auth_method
        self.auth_error_reason = reason

    def auth_error_nouser(self):
        if self.auth_error_reason in ('APIKEY_INVALID',
                                      'COOKIE_EXPIRED',
                                      'NOAUTHDATA',
                                      'USER_NOTFOUND',
                                      'USER_DISABLED'):
            return True
        else:
            return False


def session_to_user(request, session, user_id=None, or_admin=False, require_admin=False, api=False):
    if api and request.args.get('apikey'):
        auth_method = 'API'

        apikey = ApiKey.query.filter(ApiKey.key == request.args.get('apikey')).first()
        if apikey:
            user = apikey.user
        else:
            return AuthError('APIKEY_INVALID', auth_method)
    else:
        auth_method = 'COOKIE'

        if session.get('expired'):
            return AuthError('COOKIE_EXPIRED', auth_method)
        elif session.get('user_id'):
            user = session.get('user_id')
        else:
            return AuthError('NOAUTHDATA', auth_method)

    user = User.query.get(user)

    if not user:
        return AuthError('USER_NOTFOUND', auth_method)

    if not user.enabled:
        return AuthError('USER_DISABLED', auth_method)

    if require_admin and not user.role_admin:
        return AuthError('USER_NOTADMIN', auth_method)

    if user_id:
        if user_id == user.id:
            as_admin = False
        elif or_admin:
            if user.role_admin:
                as_admin = True
            else:
                return AuthError('USER_NOMATCH|NOADMIN', auth_method)
        else:
            return AuthError('USER_NOMATCH', auth_method)

    user.auth_error = False
    user.auth_method = auth_method
    if user_id and or_admin:
        user.auth_as_admin = as_admin

    if auth_method == 'API':
        apikey.use()

    return user

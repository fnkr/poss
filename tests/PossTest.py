import unittest
import uuid

from app.auth.models import User


class PossTest(unittest.TestCase):
    def setUp(self):
        from app import app
        app.config.update(
            SERVER_NAME='localhost:%s' % app.config.get('PORT')
        )
        self.app = app.test_client()
        from app import db
        self.db = db

        user = User('%s' % str(uuid.uuid4())[:8],
                    '%s@example.com' % str(uuid.uuid4())[:8],
                    '%s' % str(uuid.uuid4())[:8])
        user.role_admin = True
        self.db.session.add(user)
        self.user_admin = user

        user = User('%s' % str(uuid.uuid4())[:8],
                    '%s@example.com' % str(uuid.uuid4())[:8],
                    '%s' % str(uuid.uuid4())[:8])
        self.db.session.add(user)
        self.user_user = user

        self.baseUrl = 'http://localhost:%s' % app.config.get('PORT')

    def login(self, user):
        email = user.email
        name = user.name
        password = user.plain_password

        request = self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        assert request.status_code == 200
        assert 'Welcome %s.' % name in str(request.data)

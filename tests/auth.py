from tests.PossTest import PossTest

class AuthTest(PossTest):
    # Home
    def test_home_as_nobody(self):
        request = self.app.get('/')
        assert request.status_code == 302

    # Home as user/admin => /tests/objects.py

    # Login
    def test_login_as_nobody(self):
        request = self.app.get('/login')
        assert request.status_code == 200

    def test_login_as_user(self):
        self.login(self.user_user)
        request = self.app.get('/login')
        assert request.status_code == 302


    # Logout
    def test_logout_as_nobody(self):
        request = self.app.get('/logout')
        assert request.status_code == 302

    def test_logout_as_user(self):
        self.login(self.user_user)
        request = self.app.get('/logout')
        assert request.status_code == 403

    def test_logout_as_user_with_referer(self):
        self.login(self.user_user)
        request = self.app.get('/logout', headers={'referer': self.baseUrl})
        assert request.status_code == 302

    # Account
    def test_account_as_nobody(self):
        request = self.app.get('/admin')
        assert request.status_code == 302

    def test_account_as_user(self):
        self.login(self.user_user)
        request = self.app.get('/account')
        assert request.status_code == 200

    # TODO: edit account / with and without referer
    # TODO: add update key / with and without referer
    # TODO: remove update key / with and without referer

    # Other Account
    def test_other_account_as_nobody(self):
        request = self.app.get('/account/1')
        assert request.status_code == 302

    def test_other_account_as_user(self):
        self.login(self.user_user)
        request = self.app.get('/account/1')
        assert request.status_code == 403

    def test_other_account_as_admin(self):
        self.login(self.user_admin)
        request = self.app.get('/account/1')
        assert request.status_code == 200

    # TODO: edit account / with and without referer
    # TODO: add update key / with and without referer
    # TODO: delete update key / with and without referer

    # Admin
    def test_admin_as_nobody(self):
        request = self.app.get('/admin')
        assert request.status_code == 302

    def test_admin_as_user(self):
        self.login(self.user_user)
        request = self.app.get('/admin')
        assert request.status_code == 403

    def test_admin_as_admin(self):
        self.login(self.user_admin)
        request = self.app.get('/admin')
        assert request.status_code == 200

    # TODO: add user / with and without referer
    # TODO: delete user / with and without referer
    # TODO: lock user / with and without referer
    # TODO: unlock user / with and without referer

# TODO: test 302 targets

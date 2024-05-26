from .test_base import BaseTestCase
from blog.model import User
from flask import url_for


class UserViewsTests(BaseTestCase):
    def test_users_can_login(self):
        user = User(username='Joe', email='joe@joes.com', password='12345', full_name='Joe Smith')
        user.create()

        response = self.client.post(url_for('login'), data={'username': 'Joe', 'password': '12345'})
        self.assert_redirects(response, url_for('index'))
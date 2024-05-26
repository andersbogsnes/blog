from flask_testing import TestCase

from blog import app, extensions


class BaseTestCase(TestCase):
    """Baseclass for testing blog"""

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'posts')
    ALLOWED_EXTENSIONS = {'md'}

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    ADMINS = ['andersbogsnes@gmail.com']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
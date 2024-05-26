from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

lm = LoginManager()
db = SQLAlchemy()
lm.login_view = 'login'

migrate = Migrate()


def init_app(app: Flask) -> Flask:
    lm.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app

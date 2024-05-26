import os

from flask import Flask

from blog import extensions
from blog.views import router


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(os.getenv('APP_SETTINGS', "blog.config.DevelopmentConfig"))
    extensions.init_app(app)
    app.register_blueprint(router)
    return app

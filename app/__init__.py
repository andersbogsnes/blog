from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/blog.log', 'a', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.info("Blog startup")

    credentials = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                               'no-reply@{}'.format(app.config['MAIL_SERVER']),
                               app.config['ADMINS'], 'blog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


from app import views, model


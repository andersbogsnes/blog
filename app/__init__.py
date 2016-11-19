from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_pyfile('config.py')
app.config.from_envvar('BLOG_SETTINGS')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from app import views


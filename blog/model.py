from werkzeug.security import check_password_hash
from hashlib import md5
from blog.extensions import db
import datetime
from sqlalchemy.exc import IntegrityError


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    full_name = db.Column(db.Text)
    password = db.Column(db.Text)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, password, full_name):
        self.username = username
        self.email = email
        self.password = password
        self.full_name = full_name

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def create(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            print("User already exists")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def avatar(self, size):
        md5hash = md5(self.email.encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/avatar/{email}?d=mm&s={size}'.format(email=md5hash, size=size)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    body = db.Column(db.String)
    markdown = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
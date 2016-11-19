from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5
import app


class User:
    def __init__(self, username, email, full_name, password=None):
        self.username = username
        self.email = email
        self.full_name = full_name
        if password:
            self.pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
        self.posts = []

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def avatar(self, size):
        md5hash = md5(self.email.encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/avatar/{email}?d=mm&s={size}'.format(email=md5hash, size=size)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    def insert(self):
        db = app.config['USERS_COLLECTION']
        db.insert_one({})


class Post:
    def __init__(self, username, text, timestamp):
        self.author = username
        self.content = text
        self.timestamp = timestamp

    def insert(self):
        db = app.config['POSTS_COLLECTION']
        users = app.config['USERS_COLLECTION']
        result = db.insert_one({"author": self.author,
                                "content": self.content,
                                "timestamp": self.timestamp})
        cursor = users.find_one({"_id": self.author})


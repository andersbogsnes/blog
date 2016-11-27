import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_admin():
    from app import db
    from app.model import User
    from getpass import getpass
    from werkzeug.security import generate_password_hash

    username = input("Enter username: ")
    email = input("Enter email: ")
    password = generate_password_hash(getpass("Enter password: "))
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    full_name = "{first} {last}".format(first=first_name, last=last_name)

    admin = User(username=username, email=email, full_name=full_name, password=password)

    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
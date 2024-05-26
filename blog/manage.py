import click
from flask.cli import FlaskGroup

from blog.app import create_app
from blog.extensions import db


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command()
def create_admin():
    """Creates the admin user."""
    from blog.model import User
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
    cli()
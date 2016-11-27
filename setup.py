import argparse
from argparse import RawTextHelpFormatter


def create_db():
    from migrate.versioning import api
    from config import SQLALCHEMY_DATABASE_URI
    from config import SQLALCHEMY_MIGRATE_REPO
    from app import db
    import os.path

    print("Creating DB")

    db.create_all()

    print("Creating Migrate Repo")
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

    else:
        api.version_control(SQLALCHEMY_DATABASE_URI,
                            SQLALCHEMY_MIGRATE_REPO,
                            api.version(SQLALCHEMY_MIGRATE_REPO))

def migrate_db():
    import types
    from migrate.versioning import api
    from config import SQLALCHEMY_DATABASE_URI
    from config import SQLALCHEMY_MIGRATE_REPO
    from app import db

    print("Starting migration")
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    migration = '{}/versions/{:03d}_migration.py'.format(SQLALCHEMY_MIGRATE_REPO, v+1)
    tmp_module = types.ModuleType('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec(old_model, tmp_module.__dict__)

    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                              SQLALCHEMY_MIGRATE_REPO,
                                              tmp_module.meta,
                                              db.metadata)
    print("Writing migration script")
    open(migration, "wt").write(script)

    print("Upgrading DB")
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('New migration saved as {}'.format(migration))
    print('Current database version: {}'.format(v))


def upgrade_db():
    from migrate.versioning import api
    from config import SQLALCHEMY_DATABASE_URI
    from config import SQLALCHEMY_MIGRATE_REPO

    print("Upgrading DB")
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: {}'.format(v))


def downgrade_db():
    from migrate.versioning import api
    from config import SQLALCHEMY_DATABASE_URI
    from config import SQLALCHEMY_MIGRATE_REPO

    print("Downgrading DB")
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v-1)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print("Current database version: {}".format(v))


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
    parser = argparse.ArgumentParser(description="Setup Blog", formatter_class=RawTextHelpFormatter)

    help_text = """
    create: Initialize DB and set up migration repository
    migrate: Set up migration script and update db to newest version
    upgrade: Upgrade db one level
    downgrade: downgrade db one level
    admin: Create admin in db
    """

    parser.add_argument("action",
                        help=help_text,
                        choices=['create', 'migrate', 'upgrade', 'downgrade', 'admin'])

    args = parser.parse_args()

    cmd = {"create": create_db,
           "migrate": migrate_db,
           "upgrade": upgrade_db,
           "downgrade": downgrade_db,
           "admin": create_admin}

    cmd[args.action]()

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    collection = MongoClient()['blog']['users']

    user = input("Input username")
    password = input("Input password")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        collection.insert({"_id":user,
                           "password":pass_hash})
        print("User created")
    except DuplicateKeyError:
        print("User already in DB")

if __name__ == '__main__':
    main()




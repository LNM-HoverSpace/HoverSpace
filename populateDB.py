#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    collection = MongoClient()["hoverspace"]["users"]

    user = input("Enter your username: ")
    password = input("Enter your password: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        collection.insert({"username": user, "password": pass_hash})
        print("User created.")
    except DuplicateKeyError:
        print("User already present in DB.")


if __name__ == '__main__':
    main()

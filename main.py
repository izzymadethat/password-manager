import getpass
import bcrypt


class User:

    """Characteristics of a User using the Password Manager."""


def add_login_info():
    login_info = {}

    url = input("Add the website link: ")
    title = input("Add the title: ")
    username = input("Add username: ")
    email = input("Add email: ")
    password = input("Add password: ")

    login_info["url"] = url
    login_info["title"] = title if title else "No Title"

    login_info["username"] = username if username else email

    login_info["email"] = email

    encrypted_password = encrypt_password(password)

    login_info["password"] = encrypted_password

    return login_info


def encrypt_password(password):
    binary_password = password.encode("utf-8")

    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(binary_password, salt)

    return encrypted_password


information = add_login_info()

print(information)

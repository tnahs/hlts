#!/usr/local/bin/python3

import os
from os import getenv
from distutils.util import strtobool


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def str_to_bool(string=None, default=None):
    """ Convert environment variables to python boolean objects. """

    if string:
        return bool(strtobool(string))

    return default


class BaseConfig(object):

    APP_VERSION = "1.1.0beta"
    DB_VERSION = "1.1.0beta"

    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite")

    LOGGING_TO_STOUT = str_to_bool(getenv("LOGGING_TO_STOUT"), False)

    FLATPAGES_ROOT = "flat/static/pages/"
    FLATPAGES_EXTENSION = ".md"


# LOGGING_MAIL_SERVER = getenv("LOGGING_MAIL_SERVER")
# LOGGING_MAIL_USERNAME = getenv("LOGGING_MAIL_USERNAME")
# LOGGING_MAIL_PASSWORD = getenv("LOGGING_MAIL_PASSWORD")
# LOGGING_MAIL_PORT = int(getenv("LOGGING_MAIL_PORT") or 25)
# LOGGING_MAIL_USE_TLS = str_to_bool(getenv("LOGGING_MAIL_USE_TLS"), True)

# MAIL_SERVER = getenv("MAIL_SERVER")
# MAIL_USERNAME = getenv("MAIL_USERNAME")
# MAIL_PASSWORD = getenv("MAIL_PASSWORD")
# MAIL_PORT = int(getenv("MAIL_PORT") or 25)
# MAIL_USE_TLS = str_to_bool(getenv("MAIL_USE_TLS"), True)
# MAIL_USE_SSL = str_to_bool(getenv("MAIL_USE_SSL"), False)


# class TestingConfig(BaseConfig):

#     TESTING = True
#     BCRYPT_LOG_ROUNDS = 4
#     WTF_CSRF_ENABLED = False
#     SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

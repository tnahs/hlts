#!/usr/bin/env python

import os
from os import getenv
from distutils.util import strtobool


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def to_bool(string, default):
    if string:
        return bool(strtobool(string))
    return default


class BaseConfig(object):
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite")

    FLATPAGES_ROOT = "beta/static/pages/"
    FLATPAGES_EXTENSION = '.md'

    LOGGING_TO_STOUT = to_bool(getenv("LOGGING_TO_STOUT"), False)
    LOGGING_MAIL_SERVER = getenv("LOGGING_MAIL_SERVER")
    LOGGING_MAIL_USERNAME = getenv("LOGGING_MAIL_USERNAME")
    LOGGING_MAIL_PASSWORD = getenv("LOGGING_MAIL_PASSWORD")
    LOGGING_MAIL_PORT = int(getenv("LOGGING_MAIL_PORT") or 25)
    LOGGING_MAIL_USE_TLS = to_bool(getenv("LOGGING_MAIL_USE_TLS"), True)

    MAIL_SERVER = getenv("MAIL_SERVER")
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_PORT = int(getenv("MAIL_PORT") or 25)
    MAIL_USE_TLS = to_bool(getenv("MAIL_USE_TLS"), True)
    MAIL_USE_SSL = to_bool(getenv("MAIL_USE_SSL"), False)


class TestingConfig(BaseConfig):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

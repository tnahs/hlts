#!/usr/bin/env python

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite")

    LOGGING_TO_STOUT = os.getenv("LOGGING_TO_STOUT", False)
    LOGGING_MAIL_SERVER = os.getenv("LOGGING_MAIL_SERVER")
    LOGGING_MAIL_USERNAME = os.getenv("LOGGING_MAIL_USERNAME")
    LOGGING_MAIL_PASSWORD = os.getenv("LOGGING_MAIL_PASSWORD")
    LOGGING_MAIL_PORT = int(os.getenv("LOGGING_MAIL_PORT") or 25)
    LOGGING_MAIL_TLS = os.getenv("LOGGING_MAIL_TLS") is not None


class TestingConfig(Config):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False

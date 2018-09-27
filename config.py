#!/usr/bin/env python

import os


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGING_TO_STOUT = os.getenv("LOGGING_TO_STOUT", False)

    LOGGING_MAIL_SERVER = os.getenv("LOGGING_MAIL_SERVER")
    LOGGING_MAIL_USERNAME = os.getenv("LOGGING_MAIL_USERNAME")
    LOGGING_MAIL_PASSWORD = os.getenv("LOGGING_MAIL_PASSWORD")
    LOGGING_MAIL_PORT = int(os.getenv("LOGGING_MAIL_PORT") or 25)
    LOGGING_MAIL_TLS = os.getenv("LOGGING_MAIL_USE_TLS") is not None

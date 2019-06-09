#!/usr/local/bin/python3

import os
import pathlib
from distutils.util import strtobool


BASE_DIR = pathlib.Path(__file__).parent


def str_to_bool(string=None, default=None):
    """ Convert environment variables to python boolean objects. """

    if string:
        return bool(strtobool(string))

    return default


class BaseConfig:

    APP_VERSION = "1.1.0beta"
    DB_VERSION = "1.1.0beta"

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite'}")

    LOGGING_TO_STOUT = str_to_bool(os.getenv("LOGGING_TO_STOUT"), False)

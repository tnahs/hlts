#!/usr/local/bin/python3

from logging import StreamHandler, Formatter, INFO
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from config import BaseConfig


db = SQLAlchemy()
login = LoginManager()
bcrypt = Bcrypt()


def create_app(config=BaseConfig):

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)

    from app.main import main
    from app.user import user
    from app.errors import errors
    from app.data import data
    from app.api import api

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(errors)
    app.register_blueprint(data)
    app.register_blueprint(api, url_prefix="/api")

    login.login_view = "user.login"
    login.login_message = None

    """ Error Logging """

    if not app.debug and not app.testing:

        logging_formatter = Formatter("%(asctime)s: %(levelname)s '%(message)s' in %(pathname)s:%(lineno)d")

        # Enabled for stout logging e.g. Heroku
        if app.config["LOGGING_TO_STOUT"]:
            local_handler = StreamHandler()
        else:
            local_handler = RotatingFileHandler("logs/hlts.log", maxBytes=10240, backupCount=10)

        local_handler.setFormatter(logging_formatter)
        local_handler.setLevel(INFO)
        app.logger.addHandler(local_handler)

    return app

from app import models
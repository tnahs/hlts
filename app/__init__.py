#!/usr/bin/env python

from logging import StreamHandler, Formatter, INFO, ERROR
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_misaka import Misaka
from flask_bcrypt import Bcrypt

from config import BaseConfig


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
bcrypt = Bcrypt()
md = Misaka(fenced_code=True, underline=True, highlight=True,
            space_headers=True, superscript=True, strikethrough=True,
            autolink=True, no_intra_emphasis=True, hard_wrap=True,
            escape=False
            )


def create_app(config=BaseConfig):

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)
    md.init_app(app)
    mail.init_app(app)

    from app.user import user
    app.register_blueprint(user)

    from app.main import main
    app.register_blueprint(main)

    from app.errors import errors
    app.register_blueprint(errors)

    from app.data import data
    app.register_blueprint(data)

    from app.api import api
    app.register_blueprint(api, url_prefix="/api")

    from app.beta import beta
    app.register_blueprint(beta, url_prefix="/beta")

    login.login_view = "user.login"
    login.login_message = None

    """

    Error Logging

    """

    if not app.debug and not app.testing:

        logging_formatter = Formatter("%(asctime)s: %(levelname)s '%(message)s' in %(pathname)s:%(lineno)d")

        # Enabled for stout logging i.e. Heroku
        if app.config["LOGGING_TO_STOUT"]:
            local_handler = StreamHandler()

        else:
            local_handler = RotatingFileHandler("logs/hlts.log", maxBytes=10240, backupCount=10)

        local_handler.setFormatter(logging_formatter)
        local_handler.setLevel(INFO)
        app.logger.addHandler(local_handler)

        if app.config["LOGGING_MAIL_SERVER"]:

            server = app.config["LOGGING_MAIL_SERVER"]
            username = app.config["LOGGING_MAIL_USERNAME"]
            password = app.config["LOGGING_MAIL_PASSWORD"]
            port = app.config["LOGGING_MAIL_PORT"]

            auth = None
            if username or password:
                auth = (username, password)

            secure = None
            if app.config["LOGGING_MAIL_USE_TLS"]:
                secure = ()

            mail_handler = SMTPHandler(
                mailhost=(server, port), fromaddr="no-reply@{0}".format(server),
                toaddrs=[username], subject="HLTS Error", credentials=auth,
                secure=secure)

            mail_handler.setFormatter(logging_formatter)
            mail_handler.setLevel(ERROR)
            app.logger.addHandler(mail_handler)

    return app

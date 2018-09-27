#!/usr/bin/env python

from logging import StreamHandler, Formatter, INFO, ERROR
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_misaka import Misaka
from flask_bcrypt import Bcrypt

from config import Config


# init extensions
login = LoginManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
md = Misaka(fenced_code=True, underline=True, highlight=True,
            space_headers=True, superscript=True, strikethrough=True,
            autolink=True, no_intra_emphasis=True, hard_wrap=True,
            escape=True
            )


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    login.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    md.init_app(app)

    # load blueprints
    from app.user import user
    from app.main import main
    from app.errors import errors
    from app.io import io
    from app.api import api

    # register blueprints
    app.register_blueprint(user)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(io)
    app.register_blueprint(api, url_prefix='/api')

    from app.models import User

    # config flask-login
    login.login_view = 'user.login'
    login.login_message = None

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


    """

    Error Logging

    """

    if not app.debug and not app.testing:

        log_format = Formatter("%(asctime)s: %(levelname)s '%(message)s' in %(pathname)s:%(lineno)d")

        # Enabled for stout logging i.e. Heroku
        if app.config['LOG_TO_STOUT']:
            local_handler = StreamHandler()

        else:
            local_handler = RotatingFileHandler('logs/hlts.log', maxBytes=10240, backupCount=10)

        local_handler.setFormatter(log_format)
        local_handler.setLevel(INFO)
        app.logger.addHandler(local_handler)

        if app.config['MAIL_SERVER']:

            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()

            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=[app.config['MAIL_USERNAME']], subject='HLTS ERROR',
                credentials=auth, secure=secure)

            mail_handler.setFormatter(log_format)
            mail_handler.setLevel(ERROR)
            app.logger.addHandler(mail_handler)

    return app

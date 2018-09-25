#!/usr/bin/env python

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
    app.register_blueprint(io, url_prefix='/io')
    app.register_blueprint(api, url_prefix='/api')

    from app.models import User

    # config flask-login
    login.login_view = 'user.login'
    login.login_message = None

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

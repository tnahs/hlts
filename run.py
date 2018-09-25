from app import create_app, db

import app.defaults as AppDefaults
from app.cli import register_cli
from app.models import User, Source, Author, Tag, Collection, Annotation

from flask import request
from werkzeug.useragents import UserAgent


app = create_app()
register_cli(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Source=Source, Author=Author, Tag=Tag,
                Collection=Collection,Annotation=Annotation)


@app.context_processor
def inject_defaults():
    return dict(SOURCE_NONE=AppDefaults.SOURCE_NONE,
                AUTHOR_NONE=AppDefaults.AUTHOR_NONE,DEBUG=app.debug)


@app.context_processor
def inject_user_agent():
    return dict(USER_AGENT=UserAgent(request.headers.get('User-Agent')))
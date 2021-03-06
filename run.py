from app import create_app, db

import app.defaults as AppDefaults
from app.cli import register_cli
from app.models import User, Source, Author, Tag, Collection, Annotation
from app.tools import land_url, home_url

from flask import request
from werkzeug.useragents import UserAgent


app = create_app()
register_cli(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Source=Source, Author=Author, Tag=Tag,
                Collection=Collection, Annotation=Annotation)


@app.context_processor
def inject_defaults():
    return dict(DEBUG=app.debug, HOME_URL=home_url(), LAND_URL=land_url(),
                USER_AGENT=UserAgent(request.headers.get('User-Agent')),
                SOURCE_NONE=AppDefaults.SOURCE_NONE,
                AUTHOR_NONE=AppDefaults.AUTHOR_NONE)

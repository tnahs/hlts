#!flask/bin/python

import app.defaults as AppDefaults

from app import create_app, db
from app.models import User, Tag, Source, Annotation

from flask import request
from werkzeug.useragents import UserAgent


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """ docstring
    """
    return {
        'db': db,
        'User': User,
        'Tag': Tag,
        'Source': Source,
        'Annotation': Annotation
    }


@app.context_processor
def inject_defaults():
    """ docstring
    """
    return dict(
        SOURCE_NONE=AppDefaults.SOURCE_NONE,
        AUTHOR_NONE=AppDefaults.AUTHOR_NONE,
        DEBUG=app.debug
    )


@app.context_processor
def inject_user_agent():

    # TODO WIP for detecting when on mobile.

    user_agent = UserAgent(request.headers.get('User-Agent'))

    return dict(USER_AGENT=user_agent)

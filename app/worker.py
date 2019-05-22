#!/usr/local/bin/python3

import os
from app import celery, create_app


app = create_app()
app.app_context().push()

"""
Running a celery worker:

celery worker --app=app.worker.celery --loglevel=DEBUG
"""
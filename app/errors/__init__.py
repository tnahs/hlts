#!/usr/bin/env python

from flask import Blueprint

errors = Blueprint('errors', __name__)

from app.errors import views

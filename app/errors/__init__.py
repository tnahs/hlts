#!/usr/local/bin/python3

from flask import Blueprint

errors = Blueprint('errors', __name__, template_folder='templates')

from . import views

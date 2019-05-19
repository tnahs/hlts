#!/usr/local/bin/python3

from flask import Blueprint

data = Blueprint('data', __name__, template_folder='templates')

from . import views

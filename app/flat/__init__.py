#!/usr/bin/env python

from flask import Blueprint

flat = Blueprint('flat', __name__, template_folder='templates', static_folder='static')

from . import views

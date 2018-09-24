#!/usr/bin/env python

from flask import Blueprint

io = Blueprint('io', __name__, template_folder='templates')

from app.io import views

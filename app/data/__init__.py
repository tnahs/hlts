#!/usr/bin/env python

from flask import Blueprint

data = Blueprint('data', __name__, template_folder='templates')

from app.data import views

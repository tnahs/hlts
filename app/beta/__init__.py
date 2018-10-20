#!/usr/bin/env python

from flask import Blueprint

beta = Blueprint('beta', __name__, template_folder='templates')

from app.beta import views

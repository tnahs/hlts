#!/usr/bin/env python

from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.admin import views

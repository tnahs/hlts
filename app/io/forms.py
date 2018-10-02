#!/usr/bin/env python

from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField
from wtforms.validators import InputRequired


class RestoreDataForm(FlaskForm):
    """ annotation form
    """
    hlts_file = FileField(validators=[InputRequired()])
    confirm = BooleanField(validators=[InputRequired()])

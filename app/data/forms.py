#!/usr/local/bin/python3

from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField
from wtforms.validators import InputRequired


class RestoreDataForm(FlaskForm):

    hlts_file = FileField("select an .hlts file...", validators=[InputRequired()])
    confirm = BooleanField("i understand this will delete all my current data "
                           "and replace it with the contents of the selected "
                           "file.", validators=[InputRequired()])

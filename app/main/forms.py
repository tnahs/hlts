#!/usr/bin/env python

from flask_wtf import FlaskForm
from wtforms import Field, StringField, TextAreaField, HiddenField
from wtforms.widgets import HiddenInput
from wtforms.validators import InputRequired


class PillBox(Field):
    widget = HiddenInput()

    def _value(self):
        """ Pass data as a space delineated string which is then split in JS
        and re-constituted as javascript Pill objects.
        """
        if self.data:
            return u" ".join([x.name for x in self.data])
        else:
            return u""

    def process_formdata(self, valuelist):
        """ Overriding the process_formdata() method processes the requested
        form data back into a list of data.
        https://wtforms.readthedocs.io/en/stable/fields.html#custom-fields
        """
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(' ')]
        else:
            self.data = []


class AnnotationForm(FlaskForm):
    """ annotation form
    """
    id = HiddenField()
    passage = TextAreaField(
        validators=[InputRequired()],
        render_kw={'placeholder': 'passage'})
    notes = TextAreaField(render_kw={'placeholder': 'notes'})
    tags = PillBox()
    collections = PillBox()
    created = StringField(render_kw={'readonly': True})
    modified = StringField(render_kw={'readonly': True})
    origin = StringField(render_kw={'readonly': True})
    protected = StringField(render_kw={'readonly': True})


class SourceForm(FlaskForm):
    """ source form
    """
    name = StringField('Source', render_kw={'placeholder': 'source'})


class AuthorForm(FlaskForm):
    """ author form
    """
    name = StringField('Author', render_kw={'placeholder': 'author'})

#!/usr/bin/env python

from app.models import Tag, Collection, Source, Author

from flask import flash
from flask_wtf import FlaskForm
from wtforms import Field, StringField, TextAreaField, BooleanField, \
    HiddenField
from wtforms.widgets import HiddenInput
from wtforms.validators import InputRequired, ValidationError


class PillBox(Field):
    widget = HiddenInput()

    def _value(self):
        """ Pass data as a space delineated string which is then split in JS
        and re-constituted as javascript Pill objects.
        """
        if self.data:
            return u" ".join([p.name for p in self.data])
        else:
            return u""

    def process_formdata(self, valuelist):
        """ Overriding the process_formdata() method processes the requested
        form data back into a list of data.
        https://wtforms.readthedocs.io/en/stable/fields.html#custom-fields
        """
        if valuelist:
            self.data = valuelist[0].strip().split(" ")
            self.data = [p.strip() for p in self.data]
        else:
            self.data = []


class AnnotationForm(FlaskForm):
    """ annotation form
    """
    id = HiddenField()
    passage = TextAreaField(
        validators=[InputRequired()],
        render_kw={"placeholder": "passage"})
    source = StringField(render_kw={"placeholder": "source"})
    author = StringField(render_kw={"placeholder": "author"})
    notes = TextAreaField(render_kw={"placeholder": "notes"})
    tags = PillBox()
    collections = PillBox()
    created = StringField(render_kw={"readonly": True})
    modified = StringField(render_kw={"readonly": True})
    origin = StringField(render_kw={"readonly": True})
    protected = StringField(render_kw={"readonly": True})

    def __init__(self, *args, **kwargs):
        super(AnnotationForm, self).__init__(*args, **kwargs)

        annotation = kwargs.get("obj", None)

        if annotation is not None:
            self.source.data = annotation.source.name
            self.author.data = annotation.source.author.name


class SourceForm(FlaskForm):
    id = HiddenField()
    name = StringField(render_kw={"placeholder": "name"})
    author_name = StringField(render_kw={"placeholder": "author"})

    def validate_name(self, field):

        source = Source.query.get(self.id.data)

        try:
            source.validate_source(self.name.data, self.author_name.data)

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(self.id.data)


class AuthorForm(FlaskForm):
    id = HiddenField()
    name = StringField(render_kw={"placeholder": "name"})

    def validate_name(self, field):

        author = Author.query.get(self.id.data)

        try:
            author.name = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(self.id.data)


class TagForm(FlaskForm):
    id = HiddenField()
    pinned = BooleanField()
    name = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "name"})
    color = StringField(render_kw={"placeholder": "color"})
    description = StringField(render_kw={"placeholder": "description"})

    def validate_name(self, field):

        tag = Tag.query.get(self.id.data)

        try:
            tag.name = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(self.id.data)


class CollectionForm(FlaskForm):
    id = HiddenField()
    pinned = BooleanField()
    name = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "name"})
    color = StringField(render_kw={"placeholder": "color"})
    description = StringField(render_kw={"placeholder": "description"})

    def validate_name(self, field):

        collection = Collection.query.get(self.id.data)

        try:
            collection.name = field.data

        except AssertionError as error:
            flash(error, "flashWarning")
            raise ValidationError(self.id.data)

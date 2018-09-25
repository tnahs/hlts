#!/usr/bin/env python

import os
import uuid
import binascii
from datetime import datetime, timedelta
from dateutil.parser import parse as dateparser

import app.defaults as AppDefaults

from app import db, bcrypt

from flask import url_for
from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound


"""

How Annotations Are Created!

Annotations are connected to their Source with a one-to-many relationship.
Sources are also connected to their Author with a one-to-many relationhip. When
an Annotation Class is instanciated two things happen with respect to its
source:

First, in the Annotation Class, refresh_source() is run on the input
"source" and "author". This first checks the Source database if the
source exists by generating a UUID based on the input values of "source"
and "author". If the source is
found then the source is attached to the annotation. If not then a new Source object is
generated and added to the Source database. This then triggers the second major step
in the creating of a source.

Within the Source Class the function refresh_author() is run on the newly instanciated
Source and the same process occurs checking weather the author exists, attaching
it to the Source if it does, and creating one if it doesn't.

When an Annotation's source is edited refresh_source() must be called manually on the
Annotation after its been queried from the database.

...

How Tags Are Handled!

Annotations and Tags are connected by a many-to-many relationship. To instanchate
an Annotation with tags, the tags supplied must be a list. This list must consist
of all the tags the annotation has. There is no function to "append" tags. When an
Annotation Class is instanciated refresh_tags() is run on the imput list of
"tags". This first clears the current Annotation's tags. Then per tag, it checks
if the tag exists, if it does, it attaches it to the Annotation, if not, it creates
a new Tag entry and attaches it to the Annotation.

When an Annotation's tags are edited refresh_tags() must be called manually on the
Annotation after its been queried from the database.

...

Editing Sources! TODO

If an annotations source is edited in annotation edit page, it edits just the
one annotation's source possibly creating a new DB entry. Eventually we will
need to add an "edit source" that changes the source's attributes for all annotations
connected to this source. Trouble with this is that we need to loop through all the
different annotations that have this source and re-link them to the new UUID. We want
to do this because we're generating UUID's based on the source's attriubutes.

"""


def generate_uuid(prefix=None):

    id = str(uuid.uuid4())

    if prefix:
        id = "{0}{1}".format(prefix, id)

    id = id.upper()

    return id


def normalize_name(string, space_replacement="-"):
    return string.replace(" ", space_replacement).lower()


class ToDictMixin(object):

    @staticmethod
    def query_to_single_dict(query):

        return query.serialize()

    @staticmethod
    def query_to_multiple_dict(query):

        return [item.serialize() for item in query]

    @staticmethod
    def query_to_paginated_dict(query, endpoint, in_request, page, per_page, **kwargs):

        results = query.paginate(page=page, per_page=per_page, error_out=False)

        data = {
            'results': [
                item.serialize() for item in results.items
            ],
            '_meta': {
                'in_request': in_request,
                'per_page': per_page,
                'page': page,
                'total_pages': results.pages,
                'total_items': results.total
            },
            '_links': {
                'self': url_for(endpoint, in_request=in_request, page=page, **kwargs),
                'pages': [
                    url_for(endpoint, in_request=in_request, page=_page, **kwargs) for _page in results.iter_pages()
                ],
                'next': url_for(endpoint, in_request=in_request, page=page + 1, **kwargs) if results.has_next else None,
                'prev': url_for(endpoint, in_request=in_request, page=page - 1, **kwargs) if results.has_prev else None
            }
        }

        return data


class PingedMixin(object):

    @classmethod
    def get_recently_pinged(cls, days):

        today = datetime.utcnow()
        recent = today - timedelta(days=days)

        results = cls.query \
            .filter(cls.pinged > recent) \
            .order_by(cls.pinged.desc())

        return results


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    admin = db.Column(db.Boolean, default=AppDefaults.ADMIN)

    theme_index = db.Column(db.Integer(), default=AppDefaults.THEME_INDEX)

    results_per_page = db.Column(db.Integer(), default=AppDefaults.RESULTS_PER_PAGE)
    recent_days = db.Column(db.Integer(), default=AppDefaults.RECENT_DAYS)

    token = db.Column(db.String(), unique=True, index=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, username, password, admin):

        self.username = username
        self.password = self._hash_password(password)
        self.admin = admin

    def __repr__(self):

        return '<User id:{0} user:{1}>'.format(self.id, self.username)

    @staticmethod
    def _hash_password(password):
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def change_password(self, password, password_confirm):

        if len(password) < 5:
            return False

        if password != password_confirm:
            return False

        self.password = self._hash_password(password)

        return True

    def change_username(self, username):

        if len(username) < 3:
            return False

        self.username = username

        return True

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def new_token(self, duration=600):

        self.token = self.generate_token()
        self.token_expiration = datetime.utcnow() + timedelta(seconds=duration)

        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @property
    def token_is_fresh(self):
        return self.token_expiration > datetime.utcnow()

    @property
    def is_admin(self):
        return self.admin

    @property
    def colors(self):

        colors = []

        colors.extend([t.serialize() for t in Tag.query.all() if t.color])
        colors.extend([c.serialize() for c in Collection.query.all() if c.color])

        return colors

    @property
    def pinned_tags(self):
        return [t.serialize() for t in Tag.query.all() if t.pinned]

    @property
    def pinned_collections(self):
        return [c.serialize() for c in Collection.query.all() if c.pinned]

    @property
    def theme(self):
        """ Return the name of style sheet found in /static/css/themes.
        """
        return '{0}.css'.format(AppDefaults.THEME_CHOICES[self.theme_index][1])

    def serialize(self):
        """ Serialize user into a dictionary.
        """
        data = {
            'id': self.id,
            'username': self.username,
            'admin': self.admin,
            'results_per_page': self.results_per_page,
            'recent_days': self.recent_days,
            'colors': self.colors,
            'pinned_tags': self.pinned_tags,
            'pinned_collection': self.pinned_collections
        }

        return data


class Source(db.Model, ToDictMixin, PingedMixin):

    __tablename__ = 'sources'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), index=True)
    pinged = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.String(), db.ForeignKey('authors.id'))

    annotations = db.relationship('Annotation', backref='source', lazy='dynamic')

    def __init__(self, id=None, source_name=None, author_name=None):

        if id is not None:
            self.id = id
        else:
            self.id = generate_uuid(AppDefaults.SOURCE_PREFIX)

        self.name = source_name

        self.refresh_author(author_name=author_name)

    def __repr__(self):

        return '<Source id:{0} name:{1} author:{2}>'.format(self.id, self.name, self.author)

    def edit(self, source):

        self.name = source['name']

        self.refresh_author(author_name=source['author_name'])

    def ping(self):
        self.pinged = datetime.utcnow()

    def refresh_author(self, author_name=None):

        id = None

        if not author_name:
            id = AppDefaults.AUTHOR_NONE['ID']
            author = Author.query \
                .filter_by(id=id).first()
        else:
            author = Author.query \
                .filter_by(name=author_name).first()

        if not author:
            author = Author(id, author_name)

            db.session.add(author)

        author.ping()

        self.author_id = author.id

    @property
    def frequency(self):
        return self.annotations.count()

    def serialize(self):
        """ Serialize source into a dictionary
        """
        data = {
            'id': self.id,
            'name': self.name,
            'author': self.author.name,
            'pinged': self.pinged.isoformat(),
            'frequency': self.frequency,
        }

        return data

    @classmethod
    def remove_orphans(cls, session):
        """ Remove orphaned authors
        """
        session.query(Source) \
            .filter(Source.annotations==None) \
            .delete(synchronize_session=False)


db.event.listen(db.session, 'before_commit', Source.remove_orphans)


class Author(db.Model, ToDictMixin, PingedMixin):

    __tablename__ = 'authors'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), index=True)
    pinged = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sources = db.relationship('Source', backref='author', lazy='dynamic')

    def __init__(self, id=None, author_name=None):

        if id is not None:
            self.id = id
        else:
            self.id = generate_uuid(AppDefaults.AUTHOR_PREFIX)

        self.name = author_name

    def __repr__(self):

        return '<Author id:{0} name:{1}>'.format(self.id, self.name)

    def ping(self):
        self.pinged = datetime.utcnow()

    def edit(self, name):

        self.name = name

    @property
    def frequency(self):
        return Annotation.query \
            .join(Source) \
            .join(Author) \
            .filter(Author.name == self.name) \
            .count()

    def serialize(self):
        """ Serialize author into a dictionary
        """
        data = {
            'id': self.id,
            'name': self.name,
            'sources': [source.name for source in self.sources],
            'pinged': self.pinged,
            'frequency': self.frequency
        }

        return data

    @classmethod
    def remove_orphans(cls, session):
        """ Remove orphaned sources
        """
        session.query(Author) \
            .filter(Author.sources==None) \
            .delete(synchronize_session=False)


db.event.listen(db.session, 'before_commit', Author.remove_orphans)


annotation_tags = db.Table('annotation_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('annotation_id', db.String(), db.ForeignKey('annotations.id'))
)


class Tag(db.Model, ToDictMixin, PingedMixin):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False, index=True)
    color = db.Column(db.String())
    pinned = db.Column(db.Boolean, default=False)
    description = db.Column(db.String())
    pinged = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name):

        self.name = normalize_name(name)

    def __repr__(self):

        return '<Tag id:{0} name:{1}>'.format(self.id, self.name)

    def edit(self, tag):

        self.name = tag['name']
        self.color = tag['color']
        self.pinned = tag['pinned']
        self.description = tag['description']

    def ping(self):
        self.pinged = datetime.utcnow()

    @property
    def frequency(self):
        return self.annotations.count()

    def serialize(self):
        """ Serialize tag into a dictionary
        """
        data = {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'pinned': self.pinned,
            'description': self.description,
            'pinged': self.pinged.isoformat(),
            'frequency': self.frequency
        }

        return data

    @classmethod
    def remove_orphans(cls, session):
        """ Remove orphaned tags that are not pinned or have a color.
        """
        session.query(Tag) \
            .filter(
                ~Tag.annotations.any(),
                Tag.color==None,
                Tag.pinned==False,
                Tag.description==None) \
            .delete(synchronize_session=False)


db.event.listen(db.session, 'before_commit', Tag.remove_orphans)


annotation_collections = db.Table('annotation_collections',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id')),
    db.Column('annotation_id', db.String(), db.ForeignKey('annotations.id'))
)


class Collection(db.Model, ToDictMixin, PingedMixin):

    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False, index=True)
    color = db.Column(db.String())
    pinned = db.Column(db.Boolean, default=False)
    description = db.Column(db.String())
    pinged = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name):

        self.name = name.lower()

    def __repr__(self):

        return '<Collection id:{0} name:{1}>'.format(self.id, self.name)

    def edit(self, collection):

        self.name = collection['name']
        self.color = collection['color']
        self.pinned = collection['pinned']
        self.description = collection['description']

    def ping(self):
        self.pinged = datetime.utcnow()

    @property
    def frequency(self):
        return self.annotations.count()

    def serialize(self):
        """ Serialize collection into a dictionary
        """
        data = {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'pinned': self.pinned,
            'description': self.description,
            'pinged': self.pinged.isoformat(),
            'frequency': self.frequency
        }

        return data

    @classmethod
    def remove_orphans(cls, session):
        """ Remove orphaned collections that are not pinned or have a color.
        """
        session.query(Collection) \
            .filter(
                ~Collection.annotations.any(),
                Collection.color==None,
                Collection.pinned==False,
                Collection.description==None) \
            .delete(synchronize_session=False)


db.event.listen(db.session, 'before_commit', Tag.remove_orphans)


class AnnotationQueryMixin(object):
    """ Common queries
    """

    @staticmethod
    def get_all():

        results = Annotation.query \
            .filter_by(deleted=False) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def get_deleted():

        results = Annotation.query \
            .filter_by(deleted=True) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def get_random(count):

        results = Annotation.query \
            .filter_by(deleted=False) \
            .order_by(func.random()) \
            .limit(count) \
            .from_self()

        return results

    @staticmethod
    def get_recently_modified(days):

        today = datetime.utcnow()
        recent = today - timedelta(days=days)

        results = Annotation.query \
            .filter_by(deleted=False) \
            .filter(Annotation.created > recent) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def get_recently_created(days):

        today = datetime.utcnow()
        recent = today - timedelta(days=days)

        results = Annotation.query \
            .filter_by(deleted=False) \
            .filter(Annotation.created > recent) \
            .order_by(Annotation.created.desc())

        return results

    @staticmethod
    def query_by_id(in_request, error404=False):

        results = Annotation.query \
            .filter_by(id=in_request) \

        if error404:
            return results.first_or_404()

        return results.first()

    @staticmethod
    def query_by_source_id(in_request):

        results = Annotation.query \
            .filter_by(source_id=in_request, deleted=False) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def query_by_author_id(in_request):

        results = Annotation.query \
            .filter_by(deleted=False) \
            .join(Annotation.source) \
            .filter(Source.author_id == in_request) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def query_by_tag_name(in_request):

        try:
            tag = Tag.query.filter_by(name=in_request).one()

        except NoResultFound:

            return Annotation.query.filter_by(id=None)

        results = Annotation.query \
            .filter_by(deleted=False) \
            .filter(Annotation.tags.contains(tag)) \
            .order_by(Annotation.modified.desc())

        """ Alternate method to get tagged annotations
        results = tag.annotations \
            .filter_by(deleted=False) \
            .order_by(Annotation.modified.desc())
        """

        return results

    @staticmethod
    def query_by_collection_name(in_request):

        try:
            collection = Collection.query.filter_by(name=in_request).one()

        except NoResultFound:

            return Annotation.query.filter_by(id=None)

        results = Annotation.query \
            .filter_by(deleted=False) \
            .filter(Annotation.collections.contains(collection)) \
            .order_by(Annotation.modified.desc())

        """ Alternate method to get tagged annotations
        results = collection.annotations \
            .filter_by(deleted=False) \
            .order_by(Annotation.modified.desc())
        """

        return results


class AnnotationUtilsMixin(object):
    """ Process and return data from Annotations.
    """

    """ filter by
    """

    @staticmethod
    def filter_query_by_source_id(query, in_request):

        results = query.filter_by(source_id=in_request)

        return results

    @staticmethod
    def filter_query_by_author_id(query, in_request):

        results = query.join(Annotation.source) \
            .filter(Source.author_id == in_request)

        return results

    @staticmethod
    def filter_query_by_tag_name(query, in_request):

        try:
            tag = Tag.query.filter_by(name=in_request).one()

        except NoResultFound:

            return Annotation.query.filter_by(id=None)

        results = query.filter(Annotation.tags.contains(tag))

        return results

    @staticmethod
    def filter_query_by_collection_name(query, in_request):

        try:
            collection = Collection.query.filter_by(name=in_request).one()

        except NoResultFound:

            return Annotation.query.filter_by(id=None)

        results = query.filter(Annotation.collections.contains(collection))

        return results

    """ get x from query
    """

    @staticmethod
    def get_sources_from_query(query):
        """ Compile a dictionary of sources from query.
        """
        query = query.join(Source)

        info = []

        for source in Source.query.all():

            if query.filter(Source.name == source.name).first():

                info.append(source.serialize())

        return info

    @staticmethod
    def get_authors_from_query(query):
        """ Compile a dictionary of authors from query.
        """
        query = query.join(Source).join(Author)

        info = []

        for author in Author.query.all():

            if query.filter(Author.name == author.name).first():

                info.append(author.serialize())

        return info

    @staticmethod
    def get_tags_from_query(query):
        """ Compile a dictionary of tags from query.
        """
        query = query.join(Annotation.tags)

        info = []

        for tag in Tag.query.all():

            if query.filter(Tag.name == tag.name).first():

                info.append(tag.serialize())

        return info

    @staticmethod
    def get_collections_from_query(query):
        """ Compile a dictionary of collections from query.
        """
        query = query.join(Annotation.collections)

        info = []

        for collection in Collection.query.all():

            if query.filter(Collection.name == collection.name).first():

                info.append(collection.serialize())

        return info

    @staticmethod
    def get_untagged_from_query(query):
        """ Compile a dictionary of tags from query.
        """

        untagged = []

        for annotation in query:

            if not annotation.tags:

                untagged.append(annotation.serialize())

        return untagged


class Annotation(db.Model, ToDictMixin, AnnotationQueryMixin, AnnotationUtilsMixin):

    __tablename__ = 'annotations'

    id = db.Column(db.String(), primary_key=True, default=generate_uuid)

    source_id = db.Column(db.String(), db.ForeignKey('sources.id'))

    passage = db.Column(db.Text(), nullable=False)
    notes = db.Column(db.Text())
    tags = db.relationship("Tag",
        secondary=annotation_tags,
        backref=db.backref("annotations", lazy="dynamic"))
    collections = db.relationship("Collection",
        secondary=annotation_collections,
        backref=db.backref("annotations", lazy="dynamic"))

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    origin = db.Column(db.String(), nullable=False, default=AppDefaults.ORIGIN)
    protected = db.Column(db.Boolean, nullable=False, default=True)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, id=None):

        if id is not None:
            self.id = id

    def __repr__(self):

        return u'<Annotation id:{0}>'.format(self.id)

    @property
    def is_deleted(self):
        return self.deleted

    @property
    def is_tagged(self):
        """ Returns a boolean based on the number of tags
        """
        return bool(len(self.tags))

    @property
    def in_collection(self):
        """ Returns a boolean based on the number of collections
        """
        return bool(len(self.collections))

    def refresh_source(self, source_name=None, author_name=None):

        id = None

        if not source_name and not author_name:
            id = AppDefaults.SOURCE_NONE['ID']
            source = Source.query \
                .filter_by(id=id).first()
        else:
            source = Source.query \
                .filter_by(name=source_name) \
                .join(Author) \
                .filter(Author.name == author_name).first()

        if not source:
            source = Source(id, source_name, author_name)

            db.session.add(source)

        source.ping()

        # Link current annotation to the newly instanciated or queried Source
        self.source_id = source.id

    def refresh_tags(self, tags):
        """ tags: list
        """
        # Clear current tags
        self.tags = []

        # Remove redundant and blank list entries
        tags = set(tags)
        tags = filter(None, tags)

        for name in tags:

            tag = Tag.query.filter_by(name=name).first()

            if not tag:
                tag = Tag(name)

            tag.ping()

            self.tags.append(tag)

    def refresh_collections(self, collections):
        """ collections: list
        """
        # Clear current collections
        self.collections = []

        # Remove redundant and blank list entries
        collections = set(collections)
        collections = filter(None, collections)

        for name in collections:

            collection = Collection.query.filter_by(name=name).first()

            if not collection:
                collection = Collection(name)

            collection.ping()

            self.collections.append(collection)

    def save(self, annotation, source, author):

        self.passage = annotation['passage']
        self.notes = annotation['notes']

        self.refresh_source(
            source_name=source['name'],
            author_name=author['name'])

        self.refresh_tags(tags=annotation['tags'])

        self.refresh_collections(collections=annotation['collections'])

    def edit(self):

        self.protected = True
        self.modified = datetime.utcnow()

    def duplicate(self):

        self.protected = True
        self.modified = datetime.utcnow()
        self.passage = u'DUPLICATE\n\n{0}'.format(self.passage)

    def delete(self):
        """ soft delete
        """
        self.deleted = True

    def restore(self):
        """ restore soft delete
        """
        self.deleted = False
        self.modified = datetime.utcnow()

    def kill(self):
        """ delete
        """
        db.session.delete(self)

    def serialize(self):
        """ Serialize annotation into a dictionary

        Dates: Exported as ISO 8601 Format
        """
        data = {
            'id': self.id,
            'passage': self.passage,
            'notes': self.notes,
            'source': {
                'name': self.source.name,
                'author': self.source.author.name,
            },
            'tags': [tag.name for tag in self.tags],
            'collections': [collection.name for collection in self.collections],
            "created": self.created.isoformat(),
            "modified": self.modified.isoformat(),
            "origin": self.origin,
            "protected": self.protected,
            "deleted": self.deleted,
        }

        return data

    def deserialize(self, annotation):
        """ De-serialize annotation from a dictionary

        Dates: Supports importing only ISO 8601 Format
        """
        created = dateparser(annotation['created'])
        modified = dateparser(annotation['modified'])

        self.id = annotation['id']
        self.passage = annotation['passage']
        self.notes = annotation['notes']
        self.created = created
        self.modified = modified
        self.protected = annotation['protected']
        self.deleted = annotation['deleted']
        self.origin = annotation['origin']

        self.refresh_source(
            source_name=annotation['source']['name'],
            author_name=annotation['source']['author'])

        self.refresh_tags(tags=annotation['tags'])

        self.refresh_collections(collections=annotation['collections'])

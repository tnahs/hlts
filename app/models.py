#!/usr/local/bin/python3

import os
import re
import uuid
import binascii
from datetime import datetime, timedelta
from dateutil.parser import parse as dateparser

import app.defaults as AppDefaults

from app import db, login, bcrypt

from flask import url_for, current_app
from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import validates


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def generate_uuid(prefix=""):
    """ Genrerate UUID with an optional prefix.
    """
    uuid_ = f"{prefix}{uuid.uuid4()}"
    return uuid_.upper()


def normalize_name(string, space_replacement="-"):
    """ Normalize name for Collections and Tags.
    """
    return string.replace(" ", space_replacement).lower()


class PingedMixin:
    """ Pinged classmethod for Collections, Tags, Sources and Authors. """

    @classmethod
    def get_recently_pinged(cls, days):

        today = datetime.utcnow()
        recent = today - timedelta(days=days)

        results = cls.query \
            .filter(cls.pinged > recent) \
            .order_by(cls.pinged.desc())

        return results


class RestoreMixin:
    """ Restore classmethod for Tags and Collections. """

    @classmethod
    def restore(cls, items):
        # items: List(dict)

        for item in items:

            query = cls.query.filter_by(name=item["name"]).first()

            if not query:
                query = cls(name=item["name"])

            query.edit(item)

            db.session.add(query)


class ToDictMixin:

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
            "results": [
                item.serialize() for item in results.items
            ],
            "metadata": {
                "in_request": in_request,
                "per_page": per_page,
                "page": page,
                "total_pages": results.pages,
                "total_items": results.total
            },
            "links": {
                "self": url_for(endpoint, in_request=in_request, page=page, **kwargs),
                "pages": [
                    url_for(endpoint, in_request=in_request, page=_page, **kwargs) for _page in results.iter_pages()
                ],
                "next": url_for(endpoint, in_request=in_request, page=page + 1, **kwargs) if results.has_next else None,
                "prev": url_for(endpoint, in_request=in_request, page=page - 1, **kwargs) if results.has_prev else None
            }
        }

        return data


class AnnotationQueryMixin:
    """ Commonly used Annotation queries. """

    @staticmethod
    def get_all():

        results = Annotation.query \
            .filter_by(in_trash=False) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def get_in_trash():

        results = Annotation.query \
            .filter_by(in_trash=True) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def get_random(count=1):

        results = Annotation.query \
            .filter_by(in_trash=False) \
            .order_by(func.random()) \
            .limit(count) \
            .from_self()

        return results

    @staticmethod
    def get_recently_modified(days):

        today = datetime.utcnow()
        recent = today - timedelta(days=days)

        results = Annotation.query \
            .filter_by(in_trash=False) \
            .filter(Annotation.modified > recent) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def get_recently_created(days):

        today = datetime.utcnow()
        recent = today - timedelta(days=days)

        results = Annotation.query \
            .filter_by(in_trash=False) \
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
            .filter_by(source_id=in_request, in_trash=False) \
            .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def query_by_author_id(in_request):

        results = Annotation.query \
            .filter_by(in_trash=False) \
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
            .filter_by(in_trash=False) \
            .filter(Annotation.tags.contains(tag)) \
            .order_by(Annotation.modified.desc())

        # Alternate method to get tagged annotations.
        # results = tag.annotations \
        #     .filter_by(in_trash=False) \
        #     .order_by(Annotation.modified.desc())

        return results

    @staticmethod
    def query_by_collection_name(in_request):

        try:
            collection = Collection.query.filter_by(name=in_request).one()
        except NoResultFound:
            return Annotation.query.filter_by(id=None)

        results = Annotation.query \
            .filter_by(in_trash=False) \
            .filter(Annotation.collections.contains(collection)) \
            .order_by(Annotation.modified.desc())

        # Alternate method to get tagged annotations.
        # results = collection.annotations \
        #     .filter_by(in_trash=False) \
        #     .order_by(Annotation.modified.desc())

        return results


class AnnotationUtilsMixin:
    """ Misc utilities to process and return data from Annotations. """

    # filter_by x

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

    # Get x from query

    @staticmethod
    def get_sources_from_query(query):
        """ Compile a dictionary of sources from query. """

        query = query.join(Source)

        info = []
        for source in Source.query.all():
            if query.filter(Source.name == source.name).first():
                info.append(source.serialize())

        return info

    @staticmethod
    def get_authors_from_query(query):
        """ Compile a dictionary of authors from query. """

        query = query.join(Source).join(Author)

        info = []
        for author in Author.query.all():
            if query.filter(Author.name == author.name).first():
                info.append(author.serialize())

        return info

    @staticmethod
    def get_tags_from_query(query):
        """ Compile a dictionary of tags from query. """

        query = query.join(Annotation.tags)

        info = []
        for tag in Tag.query.all():
            if query.filter(Tag.name == tag.name).first():
                info.append(tag.serialize())

        return info

    @staticmethod
    def get_collections_from_query(query):
        """ Compile a dictionary of collections from query. """

        query = query.join(Annotation.collections)

        info = []
        for collection in Collection.query.all():
            if query.filter(Collection.name == collection.name).first():
                info.append(collection.serialize())

        return info

    @staticmethod
    def get_untagged_from_query(query):
        """ Compile a dictionary of untagged annotations from query. """

        untagged = []
        for annotation in query:
            if not annotation.tags:
                untagged.append(annotation.serialize())

        return untagged


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    fullname = db.Column(db.String(32), nullable=False, default="")
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=AppDefaults.IS_ADMIN)

    api_key = db.Column(db.String(32), unique=True, index=True)

    theme_index = db.Column(db.Integer, default=AppDefaults.THEME_INDEX)
    results_per_page = db.Column(db.Integer, default=AppDefaults.RESULTS_PER_PAGE)
    recent_days = db.Column(db.Integer, default=AppDefaults.RECENT_DAYS)

    # v1.1.0 Add

    # v1.1.0 Remove
    show_dashboard_notification = db.Column(db.Boolean, default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grant_new_api_key()

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id} username:{self.username}>"

    @staticmethod
    def _generate_api_key():
        return binascii.hexlify(os.urandom(16)).decode()

    def grant_new_api_key(self):
        self.api_key = self._generate_api_key()

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf8')

    def validate_password(self, raw_password):
        """ Validates and sets password. """

        min_length = 6
        max_length = 32

        if not min_length <= len(raw_password) <= max_length:
            raise AssertionError(f"password must be {min_length}-{max_length} characters")

        self.set_password(raw_password)

    def change_password(self, new_password, confirm_password):
        """ Confirms new password and confirmation are identical.
        Then validates the new password and sets it.
        """

        if new_password != confirm_password:
            raise ValueError("passwords do not match")

        self.validate_password(new_password)

    def check_password(self, raw_password):

        if not bcrypt.check_password_hash(self.password, raw_password):
            raise ValueError("invalid password")

        return True

    @staticmethod
    def check_user(username):

        user = User.query.filter_by(username=username).first()

        if not user:
            raise ValueError("user does not exist")

        return user

    @validates("username")
    def validate_username(self, key, username):

        min_length = 3
        max_length = 32

        if not min_length <= len(username) <= max_length:
            raise AssertionError(f"username must be {min_length}-{max_length} characters")

        if self.username != username:
            if User.query.filter(User.username == username).first():
                raise AssertionError("username already taken")

        return username

    @validates("fullname")
    def validate_fullname(self, key, fullname):

        if fullname is not None:

            min_length = 0
            max_length = 32

            if not min_length <= len(fullname) <= max_length:
                raise AssertionError(f"fullname must be less than {max_length} characters")

        return fullname

    @validates("email")
    def validate_email(self, key, email):

        min_length = 0
        max_length = 64

        if not min_length <= len(email) <= max_length:
            raise AssertionError(f"e-mail must be {min_length}-{max_length} characters")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("invalid e-mail address")

        if self.email != email:
            if User.query.filter_by(email=email).first():
                raise AssertionError("e-mail already taken")

        return email

    @validates("results_per_page")
    def validate_results_per_page(self, key, results_per_page):

        min_length = 16
        max_length = 128

        try:
            results_per_page = int(results_per_page)
        except ValueError:
            raise AssertionError("results per page must be an an integer")

        if not min_length <= results_per_page <= max_length:
            raise AssertionError(
                f"results per page must be an integer between {min_length} and {max_length}")

        return results_per_page

    @validates("recent_days")
    def validate_recent_days(self, key, recent_days):

        min_length = 1
        max_length = 90

        try:
            recent_days = int(recent_days)
        except ValueError:
            raise AssertionError("recent days must be an an integer")

        if not min_length <= recent_days <= max_length:
            raise AssertionError(
                f"recent days must be an integer between {min_length} and {max_length}")

        return recent_days

    def edit(self, data):

        self.username = data["username"]
        self.fullname = data["fullname"]
        self.email = data["email"]
        self.results_per_page = data["results_per_page"]
        self.recent_days = data["recent_days"]

    @property
    def display_name(self):
        return self.fullname if self.fullname else self.username

    @property
    def collections(self):
        return [c.serialize() for c in Collection.query.all()]

    @property
    def tags(self):
        return [t.serialize() for t in Tag.query.all()]

    @property
    def colors(self):
        return self.colored_collections + self.colored_tags

    @property
    def colored_collections(self):
        return [c.serialize() for c in Collection.query.all() if c.color]

    @property
    def colored_tags(self):
        return [t.serialize() for t in Tag.query.all() if t.color]

    @property
    def pinned_collections(self):
        return [c.serialize() for c in Collection.query.all() if c.pinned]

    @property
    def pinned_tags(self):
        return [t.serialize() for t in Tag.query.all() if t.pinned]

    @property
    def customized_collections(self):
        return [c.serialize() for c in Collection.query.all() if c.color or c.pinned or c.description]

    @property
    def customized_tags(self):
        return [t.serialize() for t in Tag.query.all() if t.color or t.pinned or t.description]

    @property
    def theme(self):
        """ Return the name of style sheet found in /static/css/themes. """
        return f"{AppDefaults.THEME_CHOICES[self.theme_index][1]}.css"

    @property
    def data(self):
        """ Serialize User Settings and Annotations into a dictionary. """

        query = Annotation.query.all()
        annotations = Annotation.query_to_multiple_dict(query)

        data = {
            "user": self.serialize(),
            "annotations": annotations,
            "metadata": {
                "app_version": current_app.config["APP_VERSION"],
                "db_version": current_app.config["DB_VERSION"],
                "export_date": datetime.utcnow().isoformat(),
                "count": {
                    "annotations": Annotation.query.count(),
                    "sources": Source.query.count(),
                    "authors": Author.query.count(),
                    "tags": Tag.query.count(),
                    "collections": Collection.query.count()
                }
            }
        }

        return data

    def serialize(self):
        """ Serialize User into a dictionary. """

        data = {
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            "settings": {
                "theme_index": self.theme_index,
                "results_per_page": self.results_per_page,
                "recent_days": self.recent_days,
            },
            "custom": {
                "tags": self.customized_tags,
                "collections": self.customized_collections,
            }
        }

        return data

    def deserialize(self, data):
        """ De-serialize User from a dictionary. """

        self.fullname = data["fullname"]
        self.theme_index = data["settings"]["theme_index"]
        self.results_per_page = data["settings"]["results_per_page"]
        self.recent_days = data["settings"]["recent_days"]

        Tag.restore(data["custom"]["tags"])
        Collection.restore(data["custom"]["collections"])


annotation_collections = db.Table("annotation_collections",
    db.Column("collection_id", db.Integer, db.ForeignKey("collections.id"), nullable=False),
    db.Column("annotation_id", db.String(64), db.ForeignKey("annotations.id"), nullable=False),
    db.PrimaryKeyConstraint("collection_id", "annotation_id")
)


class Collection(db.Model, ToDictMixin, PingedMixin, RestoreMixin):

    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False, index=True)
    color = db.Column(db.Text, default="")
    pinned = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, default="")
    pinged = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)

    def __init__(self, name):

        self.name = normalize_name(name)

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id} name:{self.name}>"

    @validates("name")
    def validate_name(self, key, name):

        min_length = 0
        max_length = 32

        if not min_length <= len(name) <= max_length:
            raise AssertionError(f"collection must be less than {max_length} characters")

        if self.name != name:
            if Collection.query.filter(Collection.name == name).first():
                raise AssertionError(f"collection '{name}' already exists")

        return name

    def edit(self, data):

        self.name = data["name"]
        self.color = data["color"]
        self.pinned = data["pinned"]
        self.description = data["description"]

    def ping(self):
        self.pinged = datetime.utcnow()

    @property
    def frequency(self):
        return self.annotations.count()

    def serialize(self):
        """ Serialize Collection into a dictionary. """

        data = {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "pinned": self.pinned,
            "description": self.description,
            "pinged": self.pinged.isoformat(),
            "frequency": self.frequency
        }

        return data

    # Disabled
    # @classmethod
    # def remove_orphans(cls, session):
    #     """ Remove orphaned Collections that are not pinned or have a color. """
    #
    #     session.query(Collection) \
    #         .filter(
    #             ~Collection.annotations.any(),
    #             Collection.color=="",
    #             Collection.pinned==False,
    #             Collection.description=="") \
    #         .delete(synchronize_session=False)


# Disabled
# db.event.listen(db.session, "before_commit", Collection.remove_orphans)


annotation_tags = db.Table("annotation_tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), nullable=False),
    db.Column("annotation_id", db.String(64), db.ForeignKey("annotations.id"), nullable=False),
    db.PrimaryKeyConstraint("tag_id", "annotation_id")
)


class Tag(db.Model, ToDictMixin, PingedMixin, RestoreMixin):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False, index=True)
    color = db.Column(db.Text, default="")
    pinned = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, default="")
    pinged = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)

    def __init__(self, name):

        self.name = normalize_name(name)

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id} name:{self.name}>"

    @validates("name")
    def validate_name(self, key, name):

        min_length = 0
        max_length = 32

        if not min_length <= len(name) <= max_length:
            raise AssertionError(f"tag must be less than {max_length} characters")

        if self.name != name:
            if Tag.query.filter(Tag.name == name).first():
                raise AssertionError(f"tag '{v}' already exists")

        return name

    def edit(self, data):

        self.name = data["name"]
        self.color = data["color"]
        self.pinned = data["pinned"]
        self.description = data["description"]

    def ping(self):
        self.pinged = datetime.utcnow()

    @property
    def frequency(self):
        return self.annotations.count()

    def serialize(self):
        """ Serialize Tag into a dictionary. """

        data = {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "pinned": self.pinned,
            "description": self.description,
            "pinged": self.pinged.isoformat(),
            "frequency": self.frequency
        }

        return data

    # Disabled
    # @classmethod
    # def remove_orphans(cls, session):
    #     """ Remove orphaned Tags that are not pinned or have a color. """
    #
    #     session.query(Tag) \
    #         .filter(
    #             ~Tag.annotations.any(),
    #             Tag.color=="",
    #             Tag.pinned==False,
    #             Tag.description=="") \
    #         .delete(synchronize_session=False)


# Disabled
# db.event.listen(db.session, "before_commit", Tag.remove_orphans)


class Source(db.Model, ToDictMixin, PingedMixin):

    __tablename__ = "sources"

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.Text, index=True)
    pinged = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)

    author_id = db.Column(db.String(64), db.ForeignKey("authors.id"))

    annotations = db.relationship("Annotation", backref="source", lazy="dynamic")

    def __init__(self, id=None, source_name=None, author_name=None):

        if id is not None:
            self.id = id
        else:
            self.id = generate_uuid(AppDefaults.SOURCE_PREFIX)

        self.name = source_name

        self.refresh_author(author_name=author_name)

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id} name:{self.name} author:{self.author.name}>"

    def validate_source(self, name, author_name):

        if self.name != name:

            source = Source.query \
                .filter_by(name=name) \
                .join(Author) \
                .filter(Author.name == author_name).first()

            if source is not None:
                raise AssertionError(f"source/author combo '{name}/{author_name}' already exists")

    def edit(self, data):

        self.name = data["name"]

        self.refresh_author(author_name=data["author_name"])

    def ping(self):
        self.pinged = datetime.utcnow()

    def refresh_author(self, author_name=None):

        id = None

        if not author_name:
            id = AppDefaults.AUTHOR_NONE["ID"]
            author = Author.query.filter_by(id=id).first()
        else:
            author = Author.query.filter_by(name=author_name).first()

        if not author:
            author = Author(id, author_name)
            db.session.add(author)

        # Ping to show in recently modified
        author.ping()

        self.author_id = author.id

    @property
    def frequency(self):
        return self.annotations.count()

    def serialize(self):
        """ Serialize Source into a dictionary. """

        data = {
            "id": self.id,
            "name": self.name,
            "author": self.author.name,
            "pinged": self.pinged.isoformat(),
            "frequency": self.frequency,
        }

        return data

    @classmethod
    def remove_orphans(cls, session):
        """ Remove orphaned Sources. """

        session.query(Source) \
            .filter(Source.annotations==None) \
            .delete(synchronize_session=False)


db.event.listen(db.session, "before_commit", Source.remove_orphans)


class Author(db.Model, ToDictMixin, PingedMixin):

    __tablename__ = "authors"

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.Text, index=True)
    pinged = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)

    sources = db.relationship("Source", backref="author", lazy="dynamic")

    def __init__(self, id=None, author_name=None):

        if id is not None:
            self.id = id
        else:
            self.id = generate_uuid(AppDefaults.AUTHOR_PREFIX)

        self.name = author_name

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id} name:{self.name}>"

    @validates("name")
    def validate_name(self, key, name):

        if self.name != name:
            if Author.query.filter_by(name=name).first():
                raise AssertionError(f"author '{name}' already exists")

        return name

    def ping(self):
        self.pinged = datetime.utcnow()

    def edit(self, data):

        self.name = data["name"]

    @property
    def frequency(self):
        return Annotation.query \
            .join(Source) \
            .join(Author) \
            .filter(Author.name == self.name) \
            .count()

    def serialize(self):
        """ Serialize Author into a dictionary. """

        data = {
            "id": self.id,
            "name": self.name,
            "sources": [source.name for source in self.sources],
            "pinged": self.pinged,
            "frequency": self.frequency
        }

        return data

    @classmethod
    def remove_orphans(cls, session):
        """ Remove orphaned Authors. """

        session.query(Author) \
            .filter(Author.sources==None) \
            .delete(synchronize_session=False)


db.event.listen(db.session, "before_commit", Author.remove_orphans)


class Annotation(db.Model, ToDictMixin, AnnotationQueryMixin, AnnotationUtilsMixin):

    __tablename__ = "annotations"

    id = db.Column(db.String(64), primary_key=True, default=generate_uuid)

    source_id = db.Column(db.String(64), db.ForeignKey("sources.id"))

    passage = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    tags = db.relationship("Tag",
        secondary=annotation_tags,
        backref=db.backref("annotations", lazy="dynamic"))
    collections = db.relationship("Collection",
        secondary=annotation_collections,
        backref=db.backref("annotations", lazy="dynamic"))

    created = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)

    origin = db.Column(db.String(64), nullable=False, default=AppDefaults.ORIGIN)
    in_trash = db.Column(db.Boolean, default=False)

    # v1.1.0 Rename to is_refreshable
    is_protected = db.Column(db.Boolean, nullable=False, default=True)

    # v1.1.0 Add
    # is_starred = db.Column(db.Boolean, nullable=False, default=False)
    # is_refreshable = db.Column(db.Boolean, nullable=False, default=False)

    # v1.1.0 Remove

    def __init__(self, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not id:
            self.id = id

    def __repr__(self):
        return f"<{self.__class__.__name__} id:{self.id}>"

    @property
    def is_tagged(self):
        """ Returns a boolean based on the number of Tags. """
        return bool(len(self.tags))

    @property
    def in_collection(self):
        """ Returns a boolean based on the number of Collections. """
        return bool(len(self.collections))

    def refresh_source(self, source_name=None, author_name=None):

        id = None

        if not source_name and not author_name:
            id = AppDefaults.SOURCE_NONE["ID"]

            source = Source.query.filter_by(id=id).first()

        else:
            source = Source.query \
                .filter_by(name=source_name) \
                .join(Author) \
                .filter(Author.name == author_name).first()

        if not source:
            source = Source(id, source_name, author_name)

            db.session.add(source)

        # Ping to show in recently modified
        source.ping()

        self.source_id = source.id

    def refresh_tags(self, tags: list):

        self.tags = []

        # Remove redundant and blank list entries
        tags = filter(None, set(tags))

        for name in tags:

            """ FIXME: This errors out if the tag is not lower-case.
            File ".../hlts/app/models.py", line 836, in validate_name
                raise AssertionError("tag '{0}' already exists".format(name))
            AssertionError: tag 'dmn' already exists
            """
            name = name.lower()

            tag = Tag.query.filter_by(name=name).first()

            if not tag:
                tag = Tag(name)

            # Ping to show in recently modified.
            tag.ping()

            self.tags.append(tag)

    def refresh_collections(self, collections):
        """ collections: list
        """

        self.collections = []

        # Remove redundant and blank list entries
        collections = filter(None, set(collections))

        for name in collections:

            """ FIXME: Added name.lower() just in case. See above FIXME for details. """
            name = name.lower()

            collection = Collection.query.filter_by(name=name).first()

            if not collection:
                collection = Collection(name)

            # Ping to show in recently modified
            collection.ping()

            self.collections.append(collection)

    def save(self, data):

        self.passage = data["passage"]
        self.notes = data["notes"]

        self.refresh_source(
            source_name=data["source"],
            author_name=data["author"])

        self.refresh_tags(tags=data["tags"])

        self.refresh_collections(collections=data["collections"])

    def edit(self):

        self.is_protected = True
        self.modified = datetime.utcnow()

    def duplicate(self):

        self.is_protected = True
        self.modified = datetime.utcnow()
        self.passage = u"DUPLICATE\n\n{0.passage}".format(self)

    def trash(self):
        """ Place in trash. """
        self.in_trash = True

    def restore(self):
        """ Remove from trash. """
        self.in_trash = False
        self.modified = datetime.utcnow()

    def delete(self):
        """ Hard delete. """
        self.source_id = None
        self.tags = []
        self.collections = []

        db.session.delete(self)

    def serialize(self):
        """ Serialize Annotation into a dictionary.

        Dates: Exported as ISO 8601 Format
        """

        data = {
            "id": self.id,
            "passage": self.passage,
            "notes": self.notes,
            "source": {
                "name": self.source.name,
                "author": self.source.author.name,
            },
            "tags": [tag.name for tag in self.tags],
            "collections": [collection.name for collection in self.collections],
            "metadata": {
                "created": self.created.isoformat(),
                "modified": self.modified.isoformat(),
                "origin": self.origin,
                "is_protected": self.is_protected,
                "in_trash": self.in_trash
            }
        }

        return data

    def deserialize(self, data):
        """ De-serialize Annotation from a dictionary.

        Dates: Supports importing only ISO 8601 Format
        """

        if data["id"]:
            self.id = data["id"]

        self.passage = data["passage"]
        self.notes = data["notes"]

        # TODO: Place dateparser in a try/except block.
        if data["metadata"]["created"]:
            self.created = dateparser(data["metadata"]["created"])

        # TODO: Place dateparser in a try/except block.
        if data["metadata"]["modified"]:
            self.modified = dateparser(data["metadata"]["modified"])

        self.is_protected = data["metadata"]["is_protected"]
        self.in_trash = data["metadata"]["in_trash"]
        self.origin = data["metadata"]["origin"]

        self.refresh_source(
            source_name=data["source"]["name"],
            author_name=data["source"]["author"])

        self.refresh_tags(tags=data["tags"])

        self.refresh_collections(collections=data["collections"])

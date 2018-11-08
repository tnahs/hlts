#!/usr/bin/env python

import pytest
import json
from random import choice, randint
from string import letters

from app.models import User, Annotation, Tag, Collection
from app.data.tools import ExportUserData

from flask import current_app


def test_user_model(session):

    """
    User Creation Defaults
    """
    string_long = "x" * 256

    u1_username = "test_user_1"
    u1_fullname = "Test User 1"
    u1_email = "test_user_1@email.com"
    u1_password = "test_password"

    """
    User1 Tests: Create User

    GIVEN a User model
    WHEN a new User is created
    THEN check if user attributes are defined correctly and if 'check_password'
         method returns proper boolean.
    """

    u1 = User(
        username=u1_username,
        fullname=u1_fullname,
        email=u1_email)
    u1.set_password(u1_password)

    session.add(u1)
    session.commit()

    assert u1.username == u1_username
    assert u1.email == u1_email
    assert u1.fullname == u1_fullname
    assert u1.is_admin is False
    assert u1.check_password(u1_password) is True
    with pytest.raises(ValueError):
        u1.check_password("wrong_password")

    """
    User1 Tests: Column value validation

    GIVEN a User object
    WHEN a column value changes is requested
    THEN ensure 'AssertionError' is raised.
    """

    # username

    with pytest.raises(AssertionError):
        u1.username = ""

    with pytest.raises(AssertionError):
        u1.username = string_long

    # password

    with pytest.raises(AssertionError):
        u1.set_password("")

    with pytest.raises(AssertionError):
        u1.set_password(string_long)

    # email

    with pytest.raises(AssertionError):
        u1.email = string_long

    with pytest.raises(AssertionError):
        u1.email = "test_user_wrong@emailcom"

    # results_per_page

    with pytest.raises(AssertionError):
        u1.results_per_page = "invalid_type"

    with pytest.raises(AssertionError):
        u1.results_per_page = 0

    with pytest.raises(AssertionError):
        u1.results_per_page = 999

    # recent_days

    with pytest.raises(AssertionError):
        u1.recent_days = "invalid_type"

    with pytest.raises(AssertionError):
        u1.recent_days = 0

    with pytest.raises(AssertionError):
        u1.recent_days = 999

    """
    User2 Tests: Ensure usernames and e-mails are unique.

    GIVEN a User object
    WHEN a column value changes is requested
    THEN ensure 'AssertionError' is raised when a non-unique 'email' or
         'username' is used.
    """

    u2_username = "test_user_2"
    u2_fullname = "Test User 2"
    u2_email = "test_user_2@email.com"
    u2_password = "test_password"

    u2 = User(
        username=u2_username,
        fullname=u2_fullname,
        email=u2_email)
    u2.set_password(u2_password)

    session.add(u2)
    session.commit()

    with pytest.raises(AssertionError):
        u2.username = u1_username

    with pytest.raises(AssertionError):
        u2.email = u1_email

    """
    New User Tests: Ensure users can't register with same username or e-mail.

    GIVEN a User model
    WHEN a new User is created
    THEN ensure 'AssertionError' is raised when a non-unique 'email' or
         'username' is used.
    """

    with pytest.raises(AssertionError):
        User(username=u1_username)

    with pytest.raises(AssertionError):
        User(email=u1_email)


def test_export_restore(session):

    """
    User Export/Restore Tests: Defaults
    """
    app = current_app._get_current_object()

    u1_username = "test_user"
    u1_fullname = "Test User"
    u1_email = "test_user@email.com"
    u1_password = "test_password"
    u1_theme_index = 0
    u1_results_per_page = 32
    u1_recent_days = 32

    """
    User Export/Restore Tests: Create User
    """

    u1 = User(
        username=u1_username,
        fullname=u1_fullname,
        email=u1_email)
    u1.set_password(u1_password)
    u1.theme_index = u1_theme_index
    u1.results_per_page = u1_results_per_page
    u1.recent_days = u1_recent_days

    session.add(u1)
    session.commit()

    """
    User Export/Restore Tests: Create Test Annotations
    """

    a1_data = {
        "passage": "Test Passage 1.",
        "source": "test-source-1",
        "author": "test-author-1",
        "tags": ["test-tag-1"],
        "collections": ["test-collection-1"],
        "notes": "test-notes-1",
    }

    a2_data = {
        "passage": "Test Passage 2.",
        "source": "test-source-2",
        "author": "test-author-2",
        "tags": ["test-tag-2"],
        "collections": ["test-collection-2"],
        "notes": "test-notes-2",
    }

    number_of_annotations = len([a1_data, a2_data])

    a1 = Annotation()
    a1.save(a1_data)
    session.add(a1)

    a2 = Annotation()
    a2.save(a2_data)
    session.add(a2)

    session.commit()

    """
    User Export/Restore Tests: Tag and Collection methods
    """

    t1_name = a1_data["tags"][0]
    c1_name = a1_data["collections"][0]

    t2_name = a2_data["tags"][0]
    c2_name = a2_data["collections"][0]

    number_of_tags = len([t1_name, t2_name])
    number_of_collections = len([c1_name, c2_name])

    t1_data = {
        "name": t1_name,
        "color": "test-color",
        "pinned": True,
        "description": "test-description",
    }

    c1_data = {
        "name": c1_name,
        "color": "test-color",
        "pinned": True,
        "description": "test-description",
    }

    t2_data = {
        "name": t2_name,
        "color": "test-color",
        "pinned": True,
        "description": "test-description",
    }

    c2_data = {
        "name": c2_name,
        "color": "test-color",
        "pinned": True,
        "description": "test-description",
    }

    tag1 = Tag.query.filter_by(name=t1_name).first()
    tag1.edit(t1_data)

    collection1 = Collection.query.filter_by(name=c1_name).first()
    collection1.edit(c1_data)

    tag2 = Tag.query.filter_by(name=t2_name).first()
    tag2.edit(t2_data)

    collection2 = Collection.query.filter_by(name=c2_name).first()
    collection2.edit(c2_data)

    session.commit()

    """
    User Export/Restore Tests: Check 'User.data' property against user defaults.

    GIVEN
    WHEN
    THEN
    """

    internal_user_data = u1.data

    assert internal_user_data["user"]["username"] == u1_username
    assert internal_user_data["user"]["fullname"] == u1_fullname
    assert internal_user_data["user"]["email"] == u1_email
    assert internal_user_data["user"]["settings"]["theme_index"] == u1_theme_index
    assert internal_user_data["user"]["settings"]["results_per_page"] == u1_results_per_page
    assert internal_user_data["user"]["settings"]["recent_days"] == u1_recent_days
    assert len(internal_user_data["user"]["custom"]["tags"]) == number_of_tags
    assert len(internal_user_data["user"]["custom"]["collections"]) == number_of_collections
    assert len(internal_user_data["annotations"]) == number_of_annotations

    """
    User Export/Restore Tests: Check 'ExportUserData.user_data' property against user defaults.

    Note: Need to convert 'export.user_data' string into Dict to read key:value pairs

    GIVEN
    WHEN
    THEN
    """

    export = ExportUserData(user=u1, context=app)

    exported_user_data = export.user_data
    exported_user_data = json.loads(exported_user_data)

    assert exported_user_data["user"]["username"] == u1_username
    assert exported_user_data["user"]["fullname"] == u1_fullname
    assert exported_user_data["user"]["email"] == u1_email
    assert exported_user_data["user"]["settings"]["theme_index"] == u1_theme_index
    assert exported_user_data["user"]["settings"]["results_per_page"] == u1_results_per_page
    assert exported_user_data["user"]["settings"]["recent_days"] == u1_recent_days
    assert len(exported_user_data["user"]["custom"]["tags"]) == number_of_tags
    assert len(exported_user_data["user"]["custom"]["collections"]) == number_of_collections
    assert len(exported_user_data["annotations"]) == number_of_annotations

    """
    User Export/Restore Tests: Restore

    FIXME This doesn't currently work...
    """

    # u2_username = "test_user_2"
    # u2_email = "test_user_2@email.com"
    # u2_password = "test_password_2"
    #
    # u2 = User(
    #     username=u2_username,
    #     email=u2_email)
    # u2.set_password(u2_password)
    #
    # session.add(u2)
    # session.commit()
    #
    # restore = RestoreUserData(user=u2, context=app)
    # restore.validate(exported_user_data)
    # restore.execute()


def test_annotation(session):

    """
    Annotation Creation Defaults
    """
    data = {
        "id": "TEST-ANNOTATION-ID",
        "passage": """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Donec sed augue ac nunc tincidunt sodales. Maecenas non commodo
            orci. Pellentesque habitant morbi tristique senectus et netus et
            malesuada fames ac turpis egestas. Interdum et malesuada fames ac
            ante ipsum primis in faucibus.""",
        "notes": "",
        "source": "Test Source",
        "author": "Test Author",
        "tags": ["t1", "t2", "t3"],
        "collections": ["c1", "c2", "c3"]
    }

    updated_data = {
        "passage": "Passage Updated",
        "notes": "Added Notes",
        "source": "Test Source Updated",
        "author": "Test Author Updated",
        "tags": ["t1-updated", "t2-updated", "t3-updated"],
        "collections": ["c1-updated", "c2-updated", "c3-updated"]
    }

    """
    Annotation1 Tests: Create Annotation

    GIVEN an Annotation model
    WHEN a new Annotation is created
    THEN check if annotation attributes are defined correctly and if
        'is_tagged' & 'in_collection' returns False and that 'tags' &
        'collections' are empty lists.
    """

    a1 = Annotation(
        id=data["id"],
        passage=data["passage"]
    )

    session.add(a1)
    session.commit()

    assert a1.passage == data["passage"]
    assert a1.deleted is False
    assert a1.protected is True
    assert a1.is_tagged is False
    assert a1.in_collection is False
    assert a1.tags == []
    assert a1.collections == []

    """
    Annotation1 Tests: Annotation Methods

    GIVEN an Annotation object
    WHEN an Annotation method is called
    THEN check if proper values are set.
    """

    a1.edit()
    assert a1.protected is True

    a1.delete()
    assert a1.deleted is True

    a1.restore()
    assert a1.deleted is False

    a1.refresh_tags(tags=data["tags"])
    assert len(a1.tags) == len(data["tags"])
    assert a1.is_tagged is True

    a1.refresh_collections(collections=data["collections"])
    assert len(a1.collections) == len(data["collections"])
    assert a1.in_collection is True

    a1.refresh_source(source_name=data["source"], author_name=data["author"])
    assert a1.source.name == data["source"]
    assert a1.source.author.name == data["author"]

    session.commit()

    a1.save(updated_data)
    session.commit()

    assert len(a1.tags) == len(updated_data["tags"])
    assert len(a1.collections) == len(updated_data["collections"])
    assert a1.passage == updated_data["passage"]
    assert a1.notes == updated_data["notes"]
    assert a1.source.name == updated_data["source"]
    assert a1.source.author.name == updated_data["author"]

    a1.kill()
    session.commit()

    a1 = Annotation.query_by_id(data["id"])
    assert a1 == None


def test_bulk_import(session):

    """
    Bulk Import Tests:

    GIVEN
    WHEN
    THEN
    """

    number_of_annotations = 25

    for i in xrange(number_of_annotations):

        string_long = xrange(randint(256, 512))
        string_short = xrange(randint(0, 128))
        number_of_collections = xrange(randint(0, 5))
        number_of_tags = xrange(randint(0, 10))

        id = "TESTING-{:04d}".format(i)
        passage = "".join([choice(letters) for x in string_long])
        notes = "".join([choice(letters) for x in string_short])
        source = "".join([choice(letters) for x in string_short])
        author = "".join([choice(letters) for x in string_short])
        tags = list({"tag-{:02d}".format(randint(0, 100)) for x in number_of_tags})
        collections = list({"collection-{:02d}".format(randint(0, 100)) for x in number_of_collections})

        data = {
            "id": id,
            "passage": passage,
            "notes": notes,
            "source": {
                "name": source,
                "author": author,
            },
            "tags": tags,
            "collections": collections,
            "created": None,
            "modified": None,
            "origin": "testing",
            "protected": False,
            "deleted": False
        }

        a = Annotation()
        a.deserialize(data)

        session.add(a)
        session.commit()

        a = Annotation.query_by_id(id)
        assert a.id == id
        assert a.passage == passage
        assert a.notes == notes
        assert a.source.name == source
        assert a.source.author.name == author
        assert len(a.tags) == len(tags)
        assert len(a.collections) == len(collections)
        assert a.protected is False
        assert a.deleted is False

        if tags:
            for name in tags:
                query = Annotation.query_by_tag_name(name).all()
                assert a in query

        if collections:
            for name in collections:
                query = Annotation.query_by_collection_name(name).all()
                assert a in query

    assert Annotation.query.count() == number_of_annotations

    for annotation in Annotation.query.all():
        annotation.kill()

    session.commit()
    assert Annotation.query.count() == 0

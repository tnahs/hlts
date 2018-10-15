#!/usr/bin/env python

import pytest

from app.models import User, Annotation, Tag, Collection


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


def test_restore(session):

    """
    User Restoration Defaults
    """
    username = "test_user"
    fullname = "Test User"
    email = "test_user@email.com"
    password = "test_password"
    restore_data = {
        "user": {
            "fullname": "Test User Restored",
            "email": "test_user_restored@email.com",
            "settings": {
                "recent_days": 30,
                "results_per_page": 25,
                "theme_index": 0
            },
            "custom": {
                "collections": [
                    {
                        "name": "test-collection",
                        "color": "test-collection-color",
                        "description": "test-collection-description",
                        "frequency": 0,
                        "id": 1,
                        "pinged": None,
                        "pinned": True
                    }
                ],
                "tags": [
                    {
                        "name": "test-tag",
                        "color": "test-tag-color",
                        "description": "test-tag-description",
                        "frequency": 0,
                        "id": 1,
                        "pinged": None,
                        "pinned": True
                    }
                ]
            }
        },
        "annotations": [
            {
                "id": "TEST-0001",
                "passage": "Test Passage 1.",
                "source": {
                    "name": "test-source",
                    "author": "test-author"
                },
                "tags": [
                    "test-tag"
                ],
                "collections": [
                    "test-collection"
                ],
                "created": None,
                "modified": None,
                "deleted": False,
                "protected": True,
                "notes": "test-notes",
                "origin": "testing-user"
            },
            {
                "id": "TEST-0002",
                "passage": "Test Passage 2.",
                "source": {
                    "name": "test-source-2",
                    "author": "test-author-2"
                },
                "tags": [
                    "test-tag"
                ],
                "collections": [
                    "test-collection"
                ],
                "created": None,
                "modified": None,
                "deleted": False,
                "protected": True,
                "notes": "test-notes-2",
                "origin": "testing-user"
            }

        ]
    }

    user = User(
        username=username,
        fullname=fullname,
        email=email)
    user.set_password(password)

    session.add(user)
    session.commit()

    """
    User Resore Tests: Check User restoration.

    GIVEN
    WHEN
    THEN
    """

    user.deserialize(restore_data["user"])
    session.commit()

    assert user.fullname == restore_data["user"]["fullname"]
    assert user.theme_index == restore_data["user"]["settings"]["theme_index"]
    assert user.results_per_page == restore_data["user"]["settings"]["results_per_page"]
    assert user.recent_days == restore_data["user"]["settings"]["recent_days"]
    assert len(user.collections) == len(restore_data["user"]["custom"]["collections"])
    assert len(user.tags) == len(restore_data["user"]["custom"]["tags"])

    """
    User Resore Tests: Check Collection restoration.

    GIVEN
    WHEN
    THEN
    """

    c_id = restore_data["user"]["custom"]["collections"][0]["id"]
    c_name = restore_data["user"]["custom"]["collections"][0]["name"]
    c_color = restore_data["user"]["custom"]["collections"][0]["color"]
    c_description = restore_data["user"]["custom"]["collections"][0]["description"]
    c_pinned = restore_data["user"]["custom"]["collections"][0]["pinned"]

    c = Collection.query.get(c_id)

    assert c.id == c_id
    assert c.name == c_name
    assert c.color == c_color
    assert c.description == c_description
    assert c.pinned == c_pinned

    """
    User Resore Tests: Check Tag restoration.

    GIVEN
    WHEN
    THEN
    """

    t_id = restore_data["user"]["custom"]["tags"][0]["id"]
    t_name = restore_data["user"]["custom"]["tags"][0]["name"]
    t_color = restore_data["user"]["custom"]["tags"][0]["color"]
    t_description = restore_data["user"]["custom"]["tags"][0]["description"]
    t_pinned = restore_data["user"]["custom"]["tags"][0]["pinned"]

    t = Tag.query.get(t_id)

    assert t.id == t_id
    assert t.name == t_name
    assert t.color == t_color
    assert t.description == t_description
    assert t.pinned == t_pinned

    """
    User Resore Tests: Check Annotation restoration.

    GIVEN
    WHEN
    THEN
    """

    for annotation in restore_data["annotations"]:
        a = Annotation()
        a.deserialize(annotation)
        session.add(a)
        session.commit()

    assert Annotation.query.count() == len(restore_data["annotations"])

    a1_id = restore_data["annotations"][0]["id"]
    a1_passage = restore_data["annotations"][0]["passage"]
    a1 = Annotation.query_by_id(a1_id)
    assert a1.passage == a1_passage

    a2_id = restore_data["annotations"][0]["id"]
    a2_passage = restore_data["annotations"][0]["passage"]
    a2 = Annotation.query_by_id(a2_id)
    assert a2.passage == a2_passage

    """
    User Resore Tests: Check 'User.data' property against 'restore_data'.

    GIVEN
    WHEN
    THEN
    """

    user_data = user.data

    assert user_data["user"]["fullname"] == restore_data["user"]["fullname"]
    assert user_data["user"]["settings"]["theme_index"] == restore_data["user"]["settings"]["theme_index"]
    assert user_data["user"]["settings"]["results_per_page"] == restore_data["user"]["settings"]["results_per_page"]
    assert user_data["user"]["settings"]["recent_days"] == restore_data["user"]["settings"]["recent_days"]
    assert len(user_data["user"]["custom"]["collections"]) == len(restore_data["user"]["custom"]["collections"])
    assert len(user_data["user"]["custom"]["tags"]) == len(restore_data["user"]["custom"]["tags"])
    assert len(user_data["annotations"]) == len(restore_data["annotations"])

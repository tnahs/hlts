#!/usr/bin/env python

from random import choice, randint
from string import letters

from app.models import Annotation


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

    Annotation.query.delete()
    session.commit()
    assert Annotation.query.count() == 0

#!/usr/bin/env python
import unittest

from app import create_app, db
from app.models import User, Annotation
from config import TestingConfig


class UserModelCase(unittest.TestCase):

    string_long = "x" * 256

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_class(self):

        user1 = User(
            username="test_user_1",
            fullname="Test User 1",
            email="test_user_1@email.com",
            admin=False)
        user1.set_password("test_password")

        db.session.add(user1)
        db.session.commit()

        """

        User1 Tests

        Test integrity of basic user creation

        """

        self.assertEqual(user1.username, "test_user_1")
        self.assertEqual(user1.fullname, "Test User 1")
        self.assertEqual(user1.email, "test_user_1@email.com")
        self.assertEqual(user1.admin, user1.is_admin)

        self.assertTrue(user1.check_password("test_password"))
        self.assertRaises(ValueError, user1.check_password, "wrong_password")

        # username

        def username_short():
            user1.username = ""
        self.assertRaises(AssertionError, username_short)

        def username_long():
            user1.username = self.string_long
        self.assertRaises(AssertionError, username_long)

        # password

        def password_short():
            user1.set_password("")
        self.assertRaises(AssertionError, password_short)

        def password_long():
            user1.set_password(self.string_long)
        self.assertRaises(AssertionError, password_long)

        # email

        def email_long():
            user1.email = self.string_long
        self.assertRaises(AssertionError, email_long)

        def email_wrong():
            user1.email = "test_user_wrong@emailcom"
        self.assertRaises(AssertionError, email_wrong)

        # results_per_page

        def results_per_page_invalid():
            user1.results_per_page = "invalid"
        self.assertRaises(AssertionError, results_per_page_invalid)

        def results_per_page_small():
            user1.results_per_page = 0
        self.assertRaises(AssertionError, results_per_page_small)

        def results_per_page_large():
            user1.results_per_page = 999
        self.assertRaises(AssertionError, results_per_page_large)

        # recent_days

        def recent_days_invalid():
            user1.recent_days = "invalid"
        self.assertRaises(AssertionError, recent_days_invalid)

        def recent_days_small():
            user1.recent_days = 0
        self.assertRaises(AssertionError, recent_days_small)

        def recent_days_large():
            user1.recent_days = 999
        self.assertRaises(AssertionError, recent_days_large)

        """

        User2 Tests

        Make sure usernames and e-mails are unique

        """

        user2 = User(
            username="test_user2",
            email="test_user_2@email.com")

        db.session.add(user2)
        db.session.commit()

        def conflict_name():
            user2.username = "test_user_1"
        self.assertRaises(AssertionError, conflict_name)

        def conflict_email():
            user2.email = "test_user_1@email.com"
        self.assertRaises(AssertionError, conflict_email)

        """

        Duplicate User Tests

        Make sure users can't register with same username or e-mail

        """

        with self.assertRaises(AssertionError):
            User(username="test_user_1")

        with self.assertRaises(AssertionError):
            User(email="test_user_1@email.com")

    def test_annotation_class(self):

        test_id = "TEST-ANNOTATION-ID"
        test_passage = """Lorem ipsum dolor sit amet, consectetur adipiscing
            elit. Donec sed augue ac nunc tincidunt sodales. Maecenas non
            commodo orci. Pellentesque habitant morbi tristique senectus et
            netus et malesuada fames ac turpis egestas. Interdum et malesuada
            fames ac ante ipsum primis in faucibus."""
        test_source = "Test Source"
        test_author = "Test Author"
        test_tags = ["t1", "t2", "t3"]
        test_collections = ["c1", "c2", "c3"]

        changed_data = {
            "passage": "Changed Passage",
            "notes": "Added Notes",
            "source": "Changed Test Source",
            "author": "Changed Test Author",
            "tags": ["t1-changed", "t2-changed", "t3-changed"],
            "collections": ["c1-changed", "c2-changed", "c3-changed"],
        }

        annotation1 = Annotation(
            id=test_id,
            passage=test_passage
        )

        db.session.add(annotation1)
        db.session.commit()

        self.assertEqual(annotation1.passage, test_passage)
        self.assertEqual(annotation1.deleted, False)
        self.assertEqual(annotation1.protected, True)
        self.assertEqual(annotation1.is_tagged, False)
        self.assertEqual(annotation1.in_collection, False)

        #

        annotation1.delete()
        self.assertEqual(annotation1.deleted, True)

        annotation1.restore()
        self.assertEqual(annotation1.deleted, False)

        annotation1.refresh_tags(test_tags)
        self.assertEqual(len(annotation1.tags), 3)
        self.assertEqual(annotation1.is_tagged, True)

        annotation1.refresh_collections(test_collections)
        self.assertEqual(len(annotation1.collections), 3)
        self.assertEqual(annotation1.in_collection, True)

        annotation1.refresh_source(
            source_name=test_source,
            author_name=test_author
        )
        self.assertEqual(annotation1.source.name, test_source)
        self.assertEqual(annotation1.source.author.name, test_author)

        #

        db.session.commit()

        #

        query_by_id = Annotation.query.get(test_id)
        self.assertEqual(query_by_id.id, test_id)

        query_by_tag0 = Annotation.query_by_tag_name(test_tags[0]).first()
        self.assertEqual(query_by_tag0.id, test_id)
        query_by_tag1 = Annotation.query_by_tag_name(test_tags[1]).first()
        self.assertEqual(query_by_tag1.id, test_id)
        query_by_tag2 = Annotation.query_by_tag_name(test_tags[2]).first()
        self.assertEqual(query_by_tag2.id, test_id)

        query_by_collection0 = Annotation.query_by_collection_name(test_collections[0]).first()
        self.assertEqual(query_by_collection0.id, test_id)
        query_by_collection1 = Annotation.query_by_collection_name(test_collections[1]).first()
        self.assertEqual(query_by_collection1.id, test_id)
        query_by_collection2 = Annotation.query_by_collection_name(test_collections[2]).first()
        self.assertEqual(query_by_collection2.id, test_id)

        #

        annotation1.save(changed_data)
        db.session.commit()

        self.assertEqual(len(annotation1.tags), 3)
        self.assertEqual(len(annotation1.collections), 3)

        self.assertEqual(annotation1.passage, changed_data["passage"])
        self.assertEqual(annotation1.notes, changed_data["notes"])
        self.assertEqual(annotation1.source.name, changed_data["source"])
        self.assertEqual(annotation1.source.author.name, changed_data["author"])

        query_by_tag0 = Annotation.query_by_tag_name(changed_data["tags"][0]).first()
        self.assertEqual(query_by_tag0.id, test_id)
        query_by_tag1 = Annotation.query_by_tag_name(changed_data["tags"][1]).first()
        self.assertEqual(query_by_tag1.id, test_id)
        query_by_tag2 = Annotation.query_by_tag_name(changed_data["tags"][2]).first()
        self.assertEqual(query_by_tag2.id, test_id)

        query_by_collection0 = Annotation.query_by_collection_name(changed_data["collections"][0]).first()
        self.assertEqual(query_by_collection0.id, test_id)
        query_by_collection1 = Annotation.query_by_collection_name(changed_data["collections"][1]).first()
        self.assertEqual(query_by_collection1.id, test_id)
        query_by_collection2 = Annotation.query_by_collection_name(changed_data["collections"][2]).first()
        self.assertEqual(query_by_tag2.id, test_id)


if __name__ == '__main__':

    unittest.main(verbosity=2)

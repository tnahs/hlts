#!/usr/bin/env python

import re
import string
from urlparse import urlparse, urljoin
from functools import wraps
from threading import Thread

from app import db
from app.models import Annotation

from flask import request, url_for, current_app


def land_url():
    return url_for('main.land')


def home_url():
    return url_for('main.dashboard')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def async_threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


class ContextThread(Thread):
    def __init__(self, *args, **kwargs):
        super(ContextThread, self).__init__(*args, **kwargs)

        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super(ContextThread, self).run()


class AsyncImport(object):

    # WIPASYNC

    def __init__(self, context):

        self.app = context

    @async_threaded
    def refresh(self, annotations):

        with self.app.app_context():

            for annotation in annotations:

                if not annotation['id']:
                    annotation['id'] = None

                existing = Annotation.query_by_id(annotation['id'])

                if existing:

                    if existing.protected:

                        continue

                    elif not existing.protected:

                        db.session.delete(existing)
                        db.session.commit()

                importing = Annotation()
                importing.deserialize(annotation)

                try:
                    db.session.add(importing)
                    db.session.commit()

                except:
                    db.session.rollback()

    @async_threaded
    def add(self, annotations):

        with self.app.app_context():

            for annotation in annotations:

                if not annotation['id']:
                    annotation['id'] = None

                existing = Annotation.query_by_id(annotation['id'])

                if existing:

                    continue

                elif not existing:

                    importing = Annotation()
                    importing.deserialize(annotation)

                    try:
                        db.session.add(importing)
                        db.session.commit()

                    except:
                        db.session.rollback()


class SortIt(object):

    @staticmethod
    def index_by_name(list_of_dictionaries, indexing_key='name'):

        index_characters = string.ascii_uppercase + string.digits

        punctuation = string.punctuation
        articles = ['the', 'an', 'a']

        punctuation = '[{0}]'.format(re.escape(punctuation))
        articles = "|".join([r"\b^{0}\b".format(a) for a in articles])

        re_punctuation = re.compile(punctuation)
        re_articles = re.compile(articles, re.IGNORECASE)

        index = {}
        for character in index_characters:

            index[character] = []

            for dictionary in list_of_dictionaries:

                name = dictionary[indexing_key]

                name = re_punctuation.sub('', name)
                name = re_articles.sub('', name)
                name = name.upper()

                if name.startswith(character):

                    index[character].append(dictionary)

        # Remove empty imdex items
        filtered_index = dict((k, v) for k, v in index.iteritems() if v)

        return filtered_index

    @staticmethod
    def by_name(list_of_dictionaries, sort_key='name'):
        return sorted(list_of_dictionaries, key=lambda k: k[sort_key], reverse=False)

    @staticmethod
    def by_frequency(list_of_dictionaries, sort_key='frequency'):
        return sorted(list_of_dictionaries, key=lambda k: k[sort_key], reverse=True)

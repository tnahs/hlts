#!/usr/bin/env python

import re
import string
from functools import wraps
from urlparse import urlparse, urljoin

from flask import current_app, request, url_for, abort
from flask_login import current_user


def land_url():
    return url_for('main.land')


def home_url():
    return url_for('main.dashboard')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


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

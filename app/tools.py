#!/usr/local/bin/python3

import re
import string
from urllib.parse import urlparse, urljoin
from functools import wraps
from threading import Thread

from app import db
from app.models import Annotation

import markdown
from flask import request, url_for, current_app, Markup


def land_url():
    return url_for("main.land")


def home_url():
    return url_for("main.dashboard")


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def async_threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


class Markdown:
    """ https://facelessuser.github.io/pymdown-extensions/
    """
    @staticmethod
    def convert(string):

        md = markdown.Markdown(
            extensions=[
                "nl2br",
                "sane_lists",
                "pymdownx.smartsymbols",
                "pymdownx.magiclink",
                "pymdownx.tasklist",
                "pymdownx.extra",
                "pymdownx.caret",
                "pymdownx.tilde",
                "pymdownx.mark",
            ]
        )

        """ http://flask.pocoo.org/docs/1.0/api/#flask.Markup
        Marks a string as being safe for inclusion in HTML/XML output without
        needing to be escaped. """
        return Markup(md.convert(string))


class SortIt:

    @staticmethod
    def build_alphabetized_index(results,
                                 indexing_key="name",
                                 ignored_articles=["the", "an", "a"]):
        """ Builds an alphabetized index i.e.
        {
            'A':
                [{'name': u'Apple'}],
            'B':
                [{'name': u'Banana'}],
            'Z':
                [{'name': u'Zucchini'}],
            '0':
                [{'name': u'007'}],
            '9':
                [{'name': u'9000'}]
        }
        results: List[dict] - Must be a list of dictionaries.
        """

        index_characters = string.ascii_uppercase + string.digits

        raw_punctuation = string.punctuation
        re_punctuation = "[{0}]".format(re.escape(raw_punctuation))
        re_compiled_punctuation = re.compile(re_punctuation)

        raw_articles = ignored_articles
        re_articles = "|".join([r"\b^{0}\b".format(a) for a in raw_articles])
        re_compiled_articles = re.compile(re_articles, re.IGNORECASE)

        index = {}

        for character in index_characters:

            index[character] = []

            for item in results:

                # Restrive sorting name from current dictionary
                sorting_name = item[indexing_key]

                # Normalize sorting_name
                sorting_name = re_compiled_punctuation.sub("", sorting_name)
                sorting_name = re_compiled_articles.sub("", sorting_name)
                sorting_name = sorting_name.strip().upper()

                if sorting_name.startswith(character):

                    index[character].append(item)

        # Remove empty index items
        filtered_index = dict((k, v) for k, v in index.items() if v)

        return filtered_index

    @staticmethod
    def by_name(results, sort_key="name"):
        """ results: List[dict] - Must be a list of dictionaries.
        """
        return sorted(results, key=lambda k: k[sort_key], reverse=False)

    @staticmethod
    def by_frequency(results, sort_key="frequency"):
        """ results: List[dict] - Must be a list of dictionaries.
        """
        return sorted(results, key=lambda k: k[sort_key], reverse=True)

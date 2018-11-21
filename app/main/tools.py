#!/usr/bin/env python

import re

from app.models import Annotation, Source, Author, Tag, Collection

from flask import render_template
from flask_login import current_user
from sqlalchemy import or_, and_


def paginated_annotations(template, endpoint, results, in_request=None, mode=None,
                          page=None, request_info=None, search_info=None):

    """ Returns the Flask "render_template" function in a standardized fashion.

    endpoint:str - Current route endpoint e.g. "main.search".

    results:Pagination object - This is always a flask_sqlalchemy Pagination
    object. Results are iterated with "results.items".

    in_request:str, dict - Or "incoming request" is the specific data requested
    by the user. For the case of main.source or main.author it would be the
    source/author UUID. For main.tags it would be the tag name. For main.search
    this is returned as a dictionary generated from SearchAnnotations() from
    main/tools.py.

    mode:str - Passes route mode. This is currently only used for main.recent
    view. But can be used for any route that has multiple modes and requires
    pagination.

    page:int - Current page number.

    request_info:Annotation/Tag/Collection/Source/Author object - Serialized if
    available to provide display information for current page.

    search_info:dict - Dictionary of parsed search query generated from
    SearchAnnotations() in main/tools.py. Accessible by calling the"info"
    property e.g. "SearchAnnotations({ query string }).info"

    """

    request_info = request_info.serialize() if request_info else None

    # Paginate results
    results = results.paginate(page=page, per_page=current_user.results_per_page, error_out=False)

    current_url = {
        "endpoint": endpoint,
        "mode": mode
    }

    return render_template(template, results=results, in_request=in_request,
                           current_url=current_url, request_info=request_info,
                           search_info=search_info)


class SearchAnnotations(object):

    search_keys = {
        "passages":     ["p", "passage", "passages"],
        "sources":      ["s", "source", "sources", "title"],
        "authors":      ["a", "author", "authors", "by"],
        "tags":         ["t", "tag", "tags"],
        "collections":  ["c", "collection", "collections"],
        "notes":        ["n", "note", "notes"]
    }

    term_min_length = 2
    key_symbols = "-:"
    bool_words_AND = ["and"]
    bool_words_OR = ["or"]
    bool_default = bool_words_OR[0]
    explicit_symbols = "\"'"

    def __init__(self, string):

        self._query = string
        self._build_search_info()

    @property
    def query(self):

        return self._build_sqla_search_query()

    @property
    def info(self):

        search_info = {
            "key": self._key,
            "bool": self._bool,
            "terms": self._terms,
            "unsafe": self._unsafe,
            "has_explicit": self._has_explicit,
            "original_query": self._query,
            "errors": self._errors,
        }

        return search_info

    def _build_search_info(self):
        """

        Parse through search string and return dictionary with
        query information.

        """

        _key = ""
        _bool = ""
        _terms = []
        _unsafe = False
        _has_explicit = False
        _errors = []

        key_pattern = r"([{0}]\w+[{0}]|\w+[{0}]|[{0}]\w+)".format(re.escape(self.key_symbols))
        key_character_pattern = r"[{0}]".format(re.escape(self.key_symbols))
        bool_pattern = r"\b({0})\b".format("|".join(self.bool_words_AND + self.bool_words_OR))
        explicit_pattern = r"[{0}][^\"']*[{0}]".format(re.escape(self.explicit_symbols))
        explicit_symbols_pattern = r"[{0}]".format(re.escape(self.explicit_symbols))

        re_key = re.compile(key_pattern)
        re_key_symbols = re.compile(key_character_pattern)
        re_bool = re.compile(bool_pattern)
        re_explicit = re.compile(explicit_pattern)
        re_explicit_symbols = re.compile(explicit_symbols_pattern)

        user_query = self._query.lower()

        """ Search for _key words.
        """
        user_search_key = re.findall(re_key, user_query)
        if user_search_key:

            if len(user_search_key) > 1:

                _unsafe = True

                _errors.append("query contains too many search keys")

            else:

                user_search_key = re.sub(re_key_symbols, "", user_search_key[0])

                for normalized_key, valid_keys in self.search_keys.items():

                    if user_search_key in valid_keys:

                        _key = normalized_key

                if not _key:

                    _unsafe = True

                    _errors.append("search key does not exists")

            # Remove _key from query.
            user_query = re.sub(re_key, "", user_query)

        """ Search for _explicit strings.
        """
        user_search_explicit = re.findall(re_explicit, user_query)
        if user_search_explicit:

            _has_explicit = True

            # Remove explicit characters from _terms
            _terms = [re.sub(re_explicit_symbols, "", explicit) for explicit in user_search_explicit]

            # Remove _explicit from query
            user_query = re.sub(re_explicit, "", user_query)

        """ Search for _bool words.
        """
        user_search_bool = re.findall(re_bool, user_query)
        if user_search_bool:

            if len(user_search_bool) > 1:

                _unsafe = True

                _errors.append("query contains too many booleans")

            else:

                _bool = user_search_bool[0]

                # Remove _bool query
                user_query = re.sub(re_bool, " ", user_query)

        else:

            _bool = self.bool_default

        """ Append remaining text to _terms.
        """
        if user_query.strip() > 0:

            _terms.extend(term.strip() for term in user_query.split(" "))

        """ If no _explicit string, split user_query into list.
        """
        if not _has_explicit:

            _terms = [term.strip() for term in user_query.split(" ")]

        """ Remove blank items in _terms
        """
        _terms = filter(None, _terms)

        """ Reject queries wth _bool but no _terms
        """
        if len(_terms) == 0:

            _unsafe = True

            _errors.append("no query terms")

        self._key = _key
        self._bool = _bool
        self._terms = _terms
        self._unsafe = _unsafe
        self._has_explicit = _has_explicit
        self._errors = _errors

    def _build_sqla_search_query(self):
        """ Build SQLAlchemy search query.
        """

        custom_query = Annotation.query \
            .filter_by(in_trash=False) \
            .join(Source) \
            .join(Author)

        filters = []

        for term in self._terms:

            if self._key:

                """

                Generates a column-specific query based on the user
                specified search key.

                """

                if self._key == "passages":
                    filters.append(
                        Annotation.passage.contains(term)
                    )

                elif self._key == "sources":
                    filters.append(
                        Source.name.contains(term)
                    )

                elif self._key == "authors":
                    filters.append(
                        Author.name.contains(term)
                    )

                elif self._key == "tags":
                    filters.append(
                        Annotation.tags.any(Tag.name.contains(term))
                    )

                elif self._key == "collections":
                    filters.append(
                        Annotation.collections.any(Collection.name.contains(term))
                    )

                elif self._key == "notes":
                    filters.append(
                        Annotation.notes.contains(term)
                    )

            else:

                """

                Generates an column independent or_ query for each term. Using
                or_ searches any of the fields. This filter is then nested
                inside an and_ or an or_ filter to compare each term in the
                list to the other.

                """

                filters.append(
                    or_(
                        Annotation.passage.contains(term),
                        Source.name.contains(term),
                        Author.name.contains(term),
                        Annotation.tags.any(Tag.name.contains(term)),
                        Annotation.collections.any(Collection.name.contains(term)),
                        Annotation.notes.contains(term)
                    )
                )

        """

        Wraps the filtered query in an and_ or or_ filter based on weather or
        not the used has used a bool keyword e.g. "and", "or".

        """

        if self._bool in self.bool_words_OR:

            return custom_query.filter(or_(*filters))

        if self._bool in self.bool_words_AND:

            return custom_query.filter(and_(*filters))

        else:

            return custom_query.filter(or_(*filters))

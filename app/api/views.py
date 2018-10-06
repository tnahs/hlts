#!/usr/bin/env python

import sys

from app.api import api

from app import db
from app.models import Annotation, Tag, Collection, Source, Author
from app.tools import SortIt
from app.api.tools import api_key_required

from flask import jsonify, g, request, current_app


@api.route('/verify_api_key', methods=['GET'])
@api_key_required
def verify_api_key():

    return jsonify({"result": "success"})


""" GET """


@api.route('/user', methods=['GET'])
@api_key_required
def user():

    return jsonify(g.current_user.serialize())


@api.route('/user/colors', methods=['GET'])
@api_key_required
def colors():

    return jsonify(g.current_user.colors)


@api.route('/user/pinned/tags', methods=['GET'])
@api_key_required
def pinned_tags():

    return jsonify(g.current_user.pinned_tags)


@api.route('/user/pinned/collections', methods=['GET'])
@api_key_required
def pinned_collections():

    return jsonify(g.current_user.pinned_collections)


@api.route('/annotations', methods=['GET'])
@api_key_required
def annotations_all():

    query = Annotation.get_all()

    data = Annotation.query_to_multiple_dict(query)

    return jsonify(data)


@api.route('/annotations/id/<string:in_request>', methods=['GET'])
@api_key_required
def annotations_by_id(in_request):

    query = Annotation.query_by_id(in_request)

    data = Annotation.query_to_single_dict(query)

    return jsonify(data)


@api.route('/annotations/tag/<string:in_request>', methods=['GET'])
@api.route('/annotations/tag/<string:in_request>/page/<int:page>', methods=['GET'])
@api_key_required
def annotations_by_tag(in_request, page=1):

    query = Annotation.query_by_tag_name(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.tag", in_request, page, per_page)

    return jsonify(data)


@api.route('/annotations/source/<string:in_request>', methods=['GET'])
@api.route('/annotations/source/<string:in_request>/page/<int:page>', methods=['GET'])
@api_key_required
def annotations_by_source(in_request, page=1):

    query = Annotation.query_by_source_id(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.source", in_request, page, per_page)

    return jsonify(data)


@api.route('/annotations/author/<string:in_request>', methods=['GET'])
@api.route('/annotations/author/<string:in_request>/page/<int:page>', methods=['GET'])
@api_key_required
def annotations_by_author(in_request, page=1):

    query = Annotation.query_by_author_id(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.author", in_request, page, per_page)

    return jsonify(data)


@api.route('/tags', methods=['GET'])
@api.route('/tags/<string:mode>', methods=['GET'])
@api_key_required
def index_tags(mode=None):

    query = Tag.query.all()
    results = Tag.query_to_multiple_dict(query)

    if mode == 'alphabetic':

        results = SortIt.by_name(results)

    elif mode == 'frequency':

        results = SortIt.by_frequency(results)

    return jsonify(results)


@api.route('/collections', methods=['GET'])
@api.route('/collections/<string:mode>', methods=['GET'])
@api_key_required
def index_collections(mode=None):

    query = Collection.query.all()
    results = Collection.query_to_multiple_dict(query)

    if mode == 'alphabetic':

        results = SortIt.by_name(results)

    elif mode == 'frequency':

        results = SortIt.by_frequency(results)

    return jsonify(results)


@api.route('/sources', methods=['GET'])
@api.route('/sources/<string:mode>', methods=['GET'])
@api_key_required
def index_sources(mode=None):

    query = Source.query.all()
    results = Source.query_to_multiple_dict(query)

    if mode == 'alphabetic':

        results = SortIt.by_name(results)

    elif mode == 'frequency':

        results = SortIt.by_frequency(results)

    return jsonify(results)


@api.route('/authors', methods=['GET'])
@api.route('/authors/<string:mode>', methods=['GET'])
@api_key_required
def index_authors(mode=None):

    query = Author.query.all()
    results = Author.query_to_multiple_dict(query)

    if mode == 'alphabetic':

        results = SortIt.by_name(results)

    elif mode == 'frequency':

        results = SortIt.by_frequency(results)

    return jsonify(results)


"""

POST

import add: Add annotation only if does not currently exist.

import refresh: Delete and re-add annotation if exists but only if unprotected.

"""


@api.route('/import/annotations/refresh', methods=['POST'])
@api_key_required
def import_annotations_refresh():

    count_added = 0
    count_protected = 0
    count_errors = 0

    annotations = request.get_json() or []

    for annotation in annotations:

        if not annotation['id']:
            annotation['id'] = None

        existing = Annotation.query_by_id(annotation['id'])

        if existing:

            if existing.protected:

                count_protected += 1

                continue

            elif not existing.protected:

                db.session.delete(existing)
                db.session.commit()

        importing = Annotation()
        importing.deserialize(annotation)

        try:
            db.session.add(importing)
            db.session.commit()

            count_added += 1

        except:
            db.session.rollback()
            current_app.logger.error(sys.exc_info())

            count_errors += 1

    payload = {
        "added": count_added,
        "protected (skipped)": count_protected,
        "errors": count_errors
    }

    response = jsonify(payload)
    response.status_code = 201
    return response


@api.route('/import/annotations/add', methods=['POST'])
@api_key_required
def import_annotations_add():

    count_added = 0
    count_existing = 0
    count_errors = 0

    annotations = request.get_json() or []

    for annotation in annotations:

        if not annotation['id']:
            annotation['id'] = None

        existing = Annotation.query_by_id(annotation['id'])

        if existing:

            count_existing += 1

            continue

        elif not existing:

            importing = Annotation()
            importing.deserialize(annotation)

            try:
                db.session.add(importing)
                db.session.commit()

                count_added += 1

            except:
                db.session.rollback()
                current_app.logger.error(sys.exc_info())

                count_errors += 1

    payload = {
        "added": count_added,
        "existing (skipped)": count_existing,
        "errors": count_errors
    }

    response = jsonify(payload)
    response.status_code = 201
    return response

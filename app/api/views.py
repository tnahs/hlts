#!/usr/bin/env python

import sys

from app.api import api

from app import db
from app.models import Annotation, Tag, Collection, Source, Author
from app.tools import SortIt
from app.api.auth import basic_auth, token_auth

from flask import jsonify, g, request, current_app


@api.route('/new_token', methods=['POST'])
@basic_auth.login_required
def new_token():

    token = g.current_user.new_token()

    db.session.commit()

    return jsonify({'token': token})


@api.route('/revoke_token', methods=['DELETE'])
@token_auth.login_required
def revoke_token():

    g.current_user.revoke_token()

    db.session.commit()

    return jsonify({'token': 'revoked'})


""" GET """


@api.route('/user', methods=['GET'])
@token_auth.login_required
def user():

    return jsonify(g.current_user.serialize())


@api.route('/user/colors', methods=['GET'])
@token_auth.login_required
def colors():

    return jsonify(g.current_user.colors)


@api.route('/user/pinned/tags', methods=['GET'])
@token_auth.login_required
def pinned_tags():

    return jsonify(g.current_user.pinned_tags)


@api.route('/user/pinned/collections', methods=['GET'])
@token_auth.login_required
def pinned_collections():

    return jsonify(g.current_user.pinned_collections)


@api.route('/annotations', methods=['GET'])
@token_auth.login_required
def annotations_all():

    query = Annotation.get_all()

    data = Annotation.query_to_multiple_dict(query)

    return jsonify(data)


@api.route('/annotations/id/<string:in_request>', methods=['GET'])
@token_auth.login_required
def annotations_by_id(in_request):

    query = Annotation.query_by_id(in_request)

    data = Annotation.query_to_single_dict(query)

    return jsonify(data)


@api.route('/annotations/tag/<string:in_request>', methods=['GET'])
@api.route('/annotations/tag/<string:in_request>/page/<int:page>', methods=['GET'])
@token_auth.login_required
def annotations_by_tag(in_request, page=1):

    query = Annotation.query_by_tag_name(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.tag", in_request, page, per_page)

    return jsonify(data)


@api.route('/annotations/source/<string:in_request>', methods=['GET'])
@api.route('/annotations/source/<string:in_request>/page/<int:page>', methods=['GET'])
@token_auth.login_required
def annotations_by_source(in_request, page=1):

    query = Annotation.query_by_source_id(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.source", in_request, page, per_page)

    return jsonify(data)


@api.route('/annotations/author/<string:in_request>', methods=['GET'])
@api.route('/annotations/author/<string:in_request>/page/<int:page>', methods=['GET'])
@token_auth.login_required
def annotations_by_author(in_request, page=1):

    query = Annotation.query_by_author_id(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.author", in_request, page, per_page)

    return data


@api.route('/tags', methods=['GET'])
@api.route('/tags/<string:mode>', methods=['GET'])
@token_auth.login_required
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
@token_auth.login_required
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
@token_auth.login_required
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
@token_auth.login_required
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

import/add: Add annotation only if does not currently exist.

import/refresh: Add annotation even if it exists but only if it is unprotected.

responses:

    - success:
    - warning:
    - error:

"""


@api.route('/import/annotations/refresh', methods=['POST'])
def import_annotations_refresh():

    annotations = request.get_json() or {}

    for annotation in annotations:

        if not annotation['id']:
            annotation['id'] = None

        existing = Annotation.query_by_id(annotation['id'])

        if existing:

            if existing.protected:

                continue

                # response = jsonify({"warning": "annotation exists and protected!"})
                # response.status_code = 201
                # return response

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
            current_app.logger.error(sys.exc_info())
            # response = jsonify({"error": "unexpected error refreshing annotation!"})
            # response.status_code = 500
            # return response

        # else:
        #     response = jsonify({"success": "annotation refreshed!"})
        #     response.status_code = 201
        #     return response

    response = jsonify({"success": "great!"})
    response.status_code = 201
    return response


@api.route('/import/annotations/add', methods=['POST'])
def import_annotations_add():

    annotations = request.get_json() or {}

    for annotation in annotations:

        if not annotation['id']:
            annotation['id'] = None

        existing = Annotation.query_by_id(annotation['id'])

        if existing:

            continue

            # response = jsonify({"warning": "annotation exists! skipped!"})
            # response.status_code = 201
            # return response

        elif not existing:

            importing = Annotation()
            importing.deserialize(annotation)

            try:
                db.session.add(importing)
                db.session.commit()

            except:
                db.session.rollback()
                current_app.logger.error(sys.exc_info())
                # response = jsonify({"error": "unexpected error refreshing annotation!"})
                # response.status_code = 500
                # return response

            # else:
            #     response = jsonify({"success": "annotation refreshed!"})
            #     response.status_code = 201
            #     return response

    response = jsonify({"success": "great!"})
    response.status_code = 201
    return response

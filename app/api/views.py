#!/usr/bin/env python

from . import api

from app.models import Annotation, Tag, Collection, Source, Author
from app.tools import SortIt, AsyncImport
from app.api.tools import api_key_required, api_error_response, api_success_response, ApiImport
from app.api.errors import ApiError
from flask import jsonify, g, request, current_app


@api.route("/verify_api_key", methods=["GET"])
@api_key_required
def verify_api_key():

    return jsonify({"result": "success"})


""" GET """


@api.route("/user", methods=["GET"])
@api_key_required
def user():

    return jsonify(g.current_user.serialize())


@api.route("/user/colors", methods=["GET"])
@api_key_required
def colors():

    return jsonify(g.current_user.colors)


@api.route("/user/pinned/collections", methods=["GET"])
@api_key_required
def pinned_collections():

    return jsonify(g.current_user.pinned_collections)


@api.route("/user/pinned/tags", methods=["GET"])
@api_key_required
def pinned_tags():

    return jsonify(g.current_user.pinned_tags)


@api.route("/annotations", methods=["GET"])
@api_key_required
def annotations_all():

    query = Annotation.get_all()

    data = Annotation.query_to_multiple_dict(query)

    return jsonify(data)


@api.route("/annotations/id/<string:in_request>", methods=["GET"])
@api_key_required
def annotations_by_id(in_request):

    query = Annotation.query_by_id(in_request)

    data = Annotation.query_to_single_dict(query)

    return jsonify(data)


@api.route("/annotations/collection/<string:in_request>", methods=["GET"])
@api.route("/annotations/collection/<string:in_request>/page/<int:page>", methods=["GET"])
@api_key_required
def annotations_by_collection(in_request, page=1):

    query = Annotation.query_by_collection_name(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.collection", in_request, page, per_page)

    return jsonify(data)


@api.route("/annotations/tag/<string:in_request>", methods=["GET"])
@api.route("/annotations/tag/<string:in_request>/page/<int:page>", methods=["GET"])
@api_key_required
def annotations_by_tag(in_request, page=1):

    query = Annotation.query_by_tag_name(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.tag", in_request, page, per_page)

    return jsonify(data)


@api.route("/annotations/source/<string:in_request>", methods=["GET"])
@api.route("/annotations/source/<string:in_request>/page/<int:page>", methods=["GET"])
@api_key_required
def annotations_by_source(in_request, page=1):

    query = Annotation.query_by_source_id(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.source", in_request, page, per_page)

    return jsonify(data)


@api.route("/annotations/author/<string:in_request>", methods=["GET"])
@api.route("/annotations/author/<string:in_request>/page/<int:page>", methods=["GET"])
@api_key_required
def annotations_by_author(in_request, page=1):

    query = Annotation.query_by_author_id(in_request)

    per_page = g.current_user.results_per_page

    data = Annotation.query_to_paginated_dict(query, "main.author", in_request, page, per_page)

    return jsonify(data)


@api.route("/collections", methods=["GET"])
@api.route("/collections/<string:mode>", methods=["GET"])
@api_key_required
def index_collections(mode=None):

    query = Collection.query.all()
    results = Collection.query_to_multiple_dict(query)

    if mode == "alphabetic":

        results = SortIt.by_name(results)

    elif mode == "frequency":

        results = SortIt.by_frequency(results)

    return jsonify(results)


@api.route("/tags", methods=["GET"])
@api.route("/tags/<string:mode>", methods=["GET"])
@api_key_required
def index_tags(mode=None):

    query = Tag.query.all()
    results = Tag.query_to_multiple_dict(query)

    if mode == "alphabetic":

        results = SortIt.by_name(results)

    elif mode == "frequency":

        results = SortIt.by_frequency(results)

    return jsonify(results)


@api.route("/sources", methods=["GET"])
@api.route("/sources/<string:mode>", methods=["GET"])
@api_key_required
def index_sources(mode=None):

    query = Source.query.all()
    results = Source.query_to_multiple_dict(query)

    if mode == "alphabetic":

        results = SortIt.by_name(results)

    elif mode == "frequency":

        results = SortIt.by_frequency(results)

    return jsonify(results)


@api.route("/authors", methods=["GET"])
@api.route("/authors/<string:mode>", methods=["GET"])
@api_key_required
def index_authors(mode=None):

    query = Author.query.all()
    results = Author.query_to_multiple_dict(query)

    if mode == "alphabetic":

        results = SortIt.by_name(results)

    elif mode == "frequency":

        results = SortIt.by_frequency(results)

    return jsonify(results)


"""

POST

import add: Add annotation only if does not currently exist.

import refresh: Delete and re-add annotation if exists but only if unprotected.

"""


@api.route("/async/import/annotations", methods=["POST"])
@api.route("/async/import/annotations/<string:mode>", methods=["POST"])
@api_key_required
def async_import_annotations(mode=None):

    # WIPASYNC

    app = current_app._get_current_object()

    annotations = request.get_json() or []

    async_import = AsyncImport(context=app)

    if mode == "add":

        async_import.add(annotations)

    elif mode == "refresh":

        async_import.refresh(annotations)

    else:

        return api_error_response(400, message="import type not selected...")

    response = jsonify({"response": "success"})
    response.status_code = 201
    return response


# NEW #########################################################################


@api.route("/error500/", methods=["GET"])
@api_key_required
def error500():

    return api_error_response(500, "Dummy Internal Server Error")


@api.route("/error400/", methods=["GET"])
@api_key_required
def error400():

    return api_error_response(400, "Dummy Bad Request Error")


@api.route("/error401/", methods=["GET"])
@api_key_required
def error401():

    return api_error_response(401, "Dummy Unauthorized Error")


@api.route("/error403/", methods=["GET"])
@api_key_required
def error403():

    return api_error_response(403, "Dummy Forbidden Error")


@api.route("/error404/", methods=["GET"])
@api_key_required
def error404():

    return api_error_response(404, "Dummy Not Found Error")


@api.route("/error405/", methods=["GET"])
@api_key_required
def error405():

    return api_error_response(405, "Dummy Method Not Allowed Error")


@api.route("/import/", methods=["POST"])
@api.route("/import/<string:mode>", methods=["POST"])
@api_key_required
def serial_import_annotations(mode=None):

    data = request.get_json() or []

    api_import = ApiImport(mode, data)

    try:
        api_import.run()
        return api_success_response()

    except ApiError as error:
        return api_error_response(error.status_code, error.message)

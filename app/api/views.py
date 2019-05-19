#!/usr/bin/env python

from . import api

from app.api.tools import ApiImport, ApiError, api_key_required
from flask import jsonify, request


# API Error Handling


@api.errorhandler(ApiError)
def handle_api_import_error(api_error):
    return api_error.send_response()


# GET


@api.route("/verify_api_key", methods=["GET"])
@api_key_required
def verify_api_key():

    return jsonify({"result": "success"})


# POST


@api.route("/import/", methods=["POST"])
@api.route("/import/<string:mode>", methods=["POST"])
@api_key_required
def import_annotations(mode=None):

    data = request.get_json() or []

    api_import = ApiImport(mode, data)
    api_import.run()

    return api_import.send_response()


# Dummy Error Responses


@api.route("/error/<int:status_code>/", methods=["GET"])
@api_key_required
def error(status_code):
    raise ApiError(status_code=status_code, message="Dummy Error")
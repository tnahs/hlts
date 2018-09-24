#!/usr/bin/env python

from app.api import api

from app.api.auth import token_auth
from app.api.ibooks.tools import IBooksSyncAPI

from flask import jsonify, request


@api.route('/sync_ibooks', methods=['POST'])
@token_auth.login_required
def sync_ibooks():

    data = request.get_json() or {}

    ibooks = IBooksSyncAPI()
    ibooks.sync_annotations(data)

    response = jsonify(ibooks.response)
    response.status_code = 201

    return response

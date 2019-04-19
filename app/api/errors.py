#!/usr/bin/env python


from flask import current_app


class Error(Exception):
    pass


class ApiError(Error):

    def __init__(self, status_code, message):

        self.status_code = status_code
        self.message = message

        current_app.logger.error("{0} Error: {1}".format(self.status_code, self.message))
#!/usr/bin/env python

from app.beta import beta

from app import pages

from flask import render_template
from flask_login import login_required


@beta.route("/")
@login_required
def main():

    page = pages.get("main")

    return render_template("beta/beta.html", page=page)


@beta.route('/<path:path>/')
@login_required
def page(path):

    page = pages.get_or_404(path)

    return render_template("beta/beta.html", page=page)

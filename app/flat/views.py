#!/usr/bin/env python

from . import flat

from app import pages

from flask import render_template
from flask_login import login_required


@flat.route("/<path:which>/")
@login_required
def page(which):

    page = pages.get_or_404(which)

    return render_template("flat/flat.html", page=page)

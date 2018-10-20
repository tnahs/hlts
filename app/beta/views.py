import os

from app.beta import beta

from flask import render_template
from flask_login import login_required


PAGES_FOLDER = os.path.join(beta.root_path + "/pages/")


@beta.route("/")
@login_required
def welcome():

    with open(PAGES_FOLDER + "welcome.md", "r") as f:
        content = f.read()

    return render_template("beta/beta.html", content=content)


@beta.route("/manual")
@login_required
def manual():

    with open(PAGES_FOLDER + "manual.md", "r") as f:
        content = f.read()

    return render_template("beta/beta.html", content=content)


@beta.route("/markdown")
@login_required
def markdown():

    with open(PAGES_FOLDER + "markdown.md", "r") as f:
        content = f.read()

    return render_template("beta/beta.html", content=content)

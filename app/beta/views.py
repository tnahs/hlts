import os

from app.beta import beta

from flask import render_template
from flask_login import login_required


MARKDOWN_FOLDER = os.path.join(beta.root_path + "/markdown/")


@beta.route("/")
@login_required
def welcome():

    with open(MARKDOWN_FOLDER + "welcome.md", "r") as f:
        content = f.read()

    return render_template("beta/beta.html", content=content)


@beta.route("/markdown")
@login_required
def markdown():

    with open(MARKDOWN_FOLDER + "using_markdown.md", "r") as f:
        content = f.read()

    return render_template("beta/beta.html", content=content)

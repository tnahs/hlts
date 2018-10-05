#!/usr/bin/env python

import random as rng
from datetime import datetime

import app.defaults as AppDefaults

from app import db
from app.models import Annotation, Source, Author, Tag, Collection
from app.tools import home_url, SortIt

from app.main import main
from app.main.forms import AnnotationForm, SourceForm, AuthorForm
from app.main.tools import SearchAnnotations, paginated_annotations

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError


"""

Main

"""


@main.route("/")
def land():

    if current_user.is_authenticated:

        return redirect(home_url())

    else:

        return redirect(url_for("user.login"))


"""

Menubar pages

"""


@main.route("/dashboard/")
@login_required
def dashboard():

    today = datetime.utcnow()

    recent_days = current_user.recent_days

    pinned_collections = current_user.pinned_collections
    pinned_tags = current_user.pinned_tags

    annotation_count = Annotation.query.count()
    tag_count = Tag.query.count()
    collection_count = Collection.query.count()

    daily_annotation = None
    daily_topic = None
    daily_topic_annotations = []

    all_annotations = Annotation.get_all()

    max_recent_tags = 40
    max_recent_collections = 10
    max_recent_sources = 10
    max_recent_authors = 10

    recent_tags = Tag.get_recently_pinged(days=recent_days).all()
    recent_collections = Collection.get_recently_pinged(days=recent_days).all()
    recent_sources = Source.get_recently_pinged(days=recent_days).all()
    recent_authors = Author.get_recently_pinged(days=recent_days).all()

    recent_tags = recent_tags[:max_recent_tags]
    recent_collections = recent_collections[:max_recent_collections]
    recent_sources = recent_sources[:max_recent_sources]
    recent_authors = recent_authors[:max_recent_authors]

    """

    Todays date as YYYYMMDD or 20180805 used to seed random number. We re-seed
    the random number with the same seed to maintain a consistent daily random
    number.

    """
    seed = int(today.strftime("%Y%m%d"))

    # Daily annotation
    if annotation_count:

        rng.seed(seed)
        random_annotation = rng.randint(1, annotation_count)

        try:
            daily_annotation = all_annotations.offset(random_annotation).first()

        except:
            daily_annotation = None

    # Topic of the day with three entries
    if tag_count and annotation_count:

        rng.seed(seed)
        random_tag = rng.randint(0, tag_count)

        try:
            daily_topic = Tag.query.offset(random_tag).first()

            daily_topic_annotations = daily_topic.annotations \
                .order_by(func.random()) \
                .paginate(page=1, per_page=3, error_out=False)

        except:
            daily_topic = None
            daily_topic_annotations = []

    dash = {
        "today": today,
        "pinned_collections": pinned_collections,
        "pinned_tags": pinned_tags,
        "annotation_count": annotation_count,
        "tag_count": tag_count,
        "collection_count": collection_count,
        "recent_tags": recent_tags,
        "recent_collections": recent_collections,
        "recent_sources": recent_sources,
        "recent_authors": recent_authors,
        "daily_annotation": daily_annotation,
        "daily_topic": daily_topic,
        "daily_topic_annotations": daily_topic_annotations
    }

    return render_template("main/dashboard.html", dash=dash)


@main.route("/index/")
@main.route("/index/<string:mode>")
@login_required
def index(mode=None):

    default_mode = "sources"

    if mode == "default" or mode == default_mode:

        request.view_args["mode"] = default_mode

        query = Source.query.all()
        results = Source.query_to_multiple_dict(query)

    elif mode == "authors":

        query = Author.query.all()
        results = Author.query_to_multiple_dict(query)

    elif mode == "tags":

        query = Tag.query.all()
        results = Tag.query_to_multiple_dict(query)

    elif mode == "collections":

        query = Collection.query.all()
        results = Collection.query_to_multiple_dict(query)

    else:

        return redirect(url_for("main.index", mode="default"))

    results = SortIt.index_by_name(results)

    return render_template("main/index.html", results=results)


@main.route("/recent/")
@main.route("/recent/page/<int:page>")
@main.route("/recent/<string:mode>/")
@main.route("/recent/<string:mode>/page/<int:page>")
@login_required
def recent(mode=None, page=1):

    default_mode = "imported"

    query = Annotation.get_recently_modified(days=current_user.recent_days)

    if mode == "default" or mode == default_mode:

        request.view_args["mode"] = default_mode

        results = query.filter_by(protected=False)

    elif mode == "edited":

        results = query.filter_by(protected=True)

    elif mode == "added":

        results = query.filter_by(origin=AppDefaults.ORIGIN)

    else:

        return redirect(url_for("main.recent", mode="default"))

    return paginated_annotations(template="main/recent.html", endpoint="main.recent", results=results, page=page, mode=mode)


@main.route("/trash/")
@main.route("/trash/page/<int:page>")
@login_required
def trash(page=1):

    results = Annotation.get_deleted()

    return paginated_annotations(template="main/trash.html", endpoint="main.trash", results=results, page=page)


@main.route("/empty_trash/")
@login_required
def empty_trash():

    for deleted in Annotation.get_deleted():
        db.session.delete(deleted)

    db.session.commit()

    return redirect(url_for("main.trash"))


"""

WIP Menubar pages

"""


@main.route("/all/")
@main.route("/all/page/<int:page>")
@login_required
def all(page=1):

    results = Annotation.get_all()

    return paginated_annotations(template="main/all.html", endpoint="main.all", results=results, page=page)


@main.route("/random/")
@login_required
def random():

    results = Annotation.get_random(count=5)

    return paginated_annotations(template="main/random.html", endpoint="main.random", results=results)


"""

Annotation querying

"""


@main.route("/source/<string:in_request>")
@main.route("/source/<string:in_request>/page/<int:page>")
@login_required
def source(in_request, page=1):

    results = Annotation.query_by_source_id(in_request)

    request_info = Source.query.filter_by(id=in_request).first()

    return paginated_annotations(template="main/source.html", endpoint="main.source",
        in_request=in_request, results=results, page=page, request_info=request_info)


@main.route("/author/<string:in_request>")
@main.route("/author/<string:in_request>/page/<int:page>")
@login_required
def author(in_request, page=1):

    results = Annotation.query_by_author_id(in_request)

    request_info = Author.query.filter_by(id=in_request).first()

    return paginated_annotations(template="main/author.html", endpoint="main.author",
        in_request=in_request, results=results, page=page, request_info=request_info)


@main.route("/tag/<string:in_request>")
@main.route("/tag/<string:in_request>/page/<int:page>")
@login_required
def tag(in_request, page=1):

    results = Annotation.query_by_tag_name(in_request)

    request_info = Tag.query.filter_by(name=in_request).first()

    return paginated_annotations(template="main/tag.html", endpoint="main.tag",
        in_request=in_request, results=results, page=page, request_info=request_info)


@main.route("/collection/<string:in_request>")
@main.route("/collection/<string:in_request>/page/<int:page>")
@login_required
def collection(in_request, page=1):

    results = Annotation.query_by_collection_name(in_request)

    request_info = Collection.query.filter_by(name=in_request).first()

    return paginated_annotations(template="main/collection.html", endpoint="main.collection",
        in_request=in_request, results=results, page=page, request_info=request_info)


@main.route("/search/", methods=["POST", "GET"])
@main.route("/search/page/<int:page>", methods=["POST", "GET"])
@login_required
def search(page=1):

    search = SearchAnnotations(request.args.get("search"))
    results = search.query
    search_info = search.info

    return paginated_annotations(template="main/search.html", endpoint="main.search", search_info=search_info,
        results=results, page=page)


"""

Adding/editing annotations

"""


@main.route("/add/", methods=["POST", "GET"])
@login_required
def add():

    form_annotation = AnnotationForm()
    form_source = SourceForm(prefix="source")
    form_author = AuthorForm(prefix="author")

    if request.method == "POST":

        if form_annotation.validate_on_submit():

            annotation = Annotation()

            annotation.save(
                form_annotation.data,
                form_source.data,
                form_author.data)

            db.session.add(annotation)
            db.session.commit()

            flash("new annotation added!", "success")

            return redirect(url_for("main.recent", mode="added"))

    return render_template("main/add.html", form_annotation=form_annotation,
        form_source=form_source, form_author=form_author)


@main.route("/edit/<string:in_request>", methods=["POST", "GET"])
@login_required
def edit(in_request):

    annotation = Annotation.query_by_id(in_request, error404=True)

    if annotation.deleted:

        flash("annotation is deleted! restore before editing!", "warning")

        return redirect(url_for("main.trash"))

    form_annotation = AnnotationForm(obj=annotation)
    form_source = SourceForm(prefix="source", obj=annotation.source)
    form_author = AuthorForm(prefix="author", obj=annotation.source.author)

    if request.method == "POST":

        if "duplicate" in request.form:

            annotation = Annotation()

            annotation.save(
                form_annotation.data,
                form_source.data,
                form_author.data)

            annotation.duplicate()

            db.session.add(annotation)
            db.session.commit()

            flash("annotation duplicated!", "success")

            return redirect(url_for("main.edit", in_request=annotation.id))

        if form_annotation.validate_on_submit():

            annotation.save(
                form_annotation.data,
                form_source.data,
                form_author.data)

            annotation.edit()

            db.session.commit()

            flash("annotation edited!", "success")

            return redirect(url_for("main.recent", mode="edited"))

    return render_template("main/edit.html", form_annotation=form_annotation,
        form_source=form_source, form_author=form_author, id=in_request)


@main.route("/delete_annotation/", methods=["POST"])
@login_required
def delete_annotation():

    in_request = request.get_json(force=True)

    id = in_request["id"]

    annotation = Annotation.query_by_id(id)

    annotation.delete()

    db.session.commit()

    return jsonify({"result": "success"})


@main.route("/restore_annotation/", methods=["POST"])
@login_required
def restore_annotation():

    in_request = request.get_json(force=True)

    id = in_request["id"]

    annotation = Annotation.query_by_id(id)

    annotation.restore()

    db.session.commit()

    return jsonify({"result": "success"})


@main.route("/kill_annotation/", methods=["POST"])
@login_required
def kill_annotation():

    in_request = request.get_json(force=True)

    id = in_request["id"]

    annotation = Annotation.query_by_id(id)

    annotation.kill()

    db.session.commit()

    return jsonify({"result": "success"})


"""

Bulk editing

"""


@main.route("/edit/sources", methods=["POST", "GET"])
@main.route("/edit/sources/page/<int:page>", methods=["POST", "GET"])
@login_required
def edit_sources(page=1, in_request=None):

    results = Source.query

    if request.method == "POST":

        form_data = request.form.copy()
        form_data["pinned"] = True if request.form.get("pinned") else False

        source = Source.query.get(form_data["id"])

        source.edit(form_data)

        db.session.commit()

        results = Source.query

    results = results.order_by(Source.name)

    results = results.paginate(page=page, per_page=current_user.results_per_page, error_out=False)

    pages = [url_for("main.edit_sources", in_request=in_request, page=pg) for pg in results.iter_pages()]

    return render_template("main/bulk.html", results=results, in_request=in_request, page=page, pages=pages)


@main.route("/edit/authors", methods=["POST", "GET"])
@main.route("/edit/authors/page/<int:page>", methods=["POST", "GET"])
@login_required
def edit_authors(page=1, in_request=None):

    results = Author.query

    if request.method == "POST":

        form_data = request.form.copy()
        form_data["pinned"] = True if request.form.get("pinned") else False

        author = Author.query.get(form_data["id"])

        author.edit(form_data["name"])

        db.session.commit()

        results = Author.query

    results = results.order_by(Author.name)

    results = results.paginate(page=page, per_page=current_user.results_per_page, error_out=False)

    pages = [url_for("main.edit_authors", in_request=in_request, page=pg) for pg in results.iter_pages()]

    return render_template("main/bulk.html", results=results, in_request=in_request, page=page, pages=pages)


@main.route("/edit/tags", methods=["POST", "GET"])
@main.route("/edit/tags/page/<int:page>", methods=["POST", "GET"])
@login_required
def edit_tags(page=1, in_request=None):

    results = Tag.query

    if request.method == "POST":

        form_data = request.form.copy()
        form_data["pinned"] = True if request.form.get("pinned") else False

        tag = Tag.query.get(form_data["id"])

        try:

            tag.edit(form_data)

            db.session.commit()

            results = Tag.query

        except IntegrityError:

            flash("the tag '{0}' already exits!".format(request.form["name"]), "warning")

            return redirect(url_for("main.edit_tags", page=page))

    results = results.order_by(Tag.pinned.desc(), Tag.name)

    results = results.paginate(page=page, per_page=current_user.results_per_page, error_out=False)

    pages = [url_for("main.edit_tags", in_request=in_request, page=pg) for pg in results.iter_pages()]

    return render_template("main/bulk.html", results=results, in_request=in_request, page=page, pages=pages)


@main.route("/edit/collections", methods=["POST", "GET"])
@main.route("/edit/collections/page/<int:page>", methods=["POST", "GET"])
@login_required
def edit_collections(page=1, in_request=None):

    results = Collection.query

    if request.method == "POST":

        form_data = request.form.copy()
        form_data["pinned"] = True if request.form.get("pinned") else False

        collection = Collection.query.get(form_data["id"])

        try:

            collection.edit(form_data)

            db.session.commit()

            results = Collection.query

        except IntegrityError:

            flash("the collection '{0}' already exits!".format(request.form["name"]), "warning")

            return redirect(url_for("main.edit_collections", page=page))

    results = results.order_by(Collection.pinned.desc(), Collection.name)

    results = results.paginate(page=page, per_page=current_user.results_per_page, error_out=False)

    pages = [url_for("main.edit_collections", in_request=in_request, page=pg) for pg in results.iter_pages()]

    return render_template("main/bulk.html", results=results, in_request=in_request, page=page, pages=pages)


"""

tools

"""


@main.route("/tools")
@login_required
def tools():

    return render_template("main/tools.html")


"""

AJAX routes

"""


@main.route("/ajax/user")
@login_required
def ajax_user_notable_items():

    return jsonify(current_user.serialize())


@main.route("/ajax/colors")
@login_required
def ajax_colors():

    return jsonify(current_user.colors)


@main.route("/ajax/pinned/tags")
@login_required
def ajax_pinned_tags():

    return jsonify(current_user.pinned_tags)


@main.route("/ajax/pinned/collections")
@login_required
def ajax_pinned_collections():

    return jsonify(current_user.pinned_collections)


@main.route("/ajax/tags")
@login_required
def ajax_tags():

    query = Tag.query.all()
    result = Tag.query_to_multiple_dict(query)

    return jsonify(result)


@main.route("/ajax/collections")
@login_required
def ajax_collections():

    query = Collection.query.all()
    result = Collection.query_to_multiple_dict(query)

    return jsonify(result)


@main.route("/ajax/sources")
@login_required
def ajax_sources():

    query = Source.query.all()
    result = Source.query_to_multiple_dict(query)

    return jsonify(result)


@main.route("/ajax/authors")
@login_required
def ajax_authors():

    query = Author.query.all()
    result = Author.query_to_multiple_dict(query)

    return jsonify(result)

def tfilter_annotations(results, endpoint, in_request, page, mode, display_limit=40):

    """
    # Snippet was in annotation_view()
    #
    # TODO Can we handle passing data better?
    if tfilter_show:
        tfiltered = tfilter_annotations(results, endpoint,
            in_request, page, mode, display_limit=None)
        results = tfiltered[0]  # results
        tfilter = tfiltered[1]  # data

    else:
        tfilter = None
    """

    all_tags_from_query = Annotation.get_tags_from_query(results)

    all_tags = [tag["name"] for tag in all_tags_from_query]

    if all_tags and request.endpoint == "main.tag":

        all_tags.remove(in_request)

    available_tags = list(all_tags)

    search = request.args.get("search")

    try:

        current_tfilters = request.args.get("filters").split(" ")

    except AttributeError:

        _enabled = False

        current_tfilters = []

    else:

        _enabled = True

        filters = [Annotation.tags.any(Tag.name == tf) for tf in current_tfilters]
        results = results.filter(and_(*filters))

        filtered_tags_from_query = Annotation.get_tags_from_query(results)
        available_tags = [tag["name"] for tag in filtered_tags_from_query]

    _data = []

    for tag in all_tags:

        new_tfilters = list(current_tfilters)

        if tag in current_tfilters:

            new_tfilters.remove(tag)
            status = "selected"
            enabled = True

        elif tag not in available_tags:

            new_tfilters = None
            status = "unavailable"
            enabled = False

        else:

            new_tfilters.append(tag)
            status = "available"
            enabled = True

        #
        new_tfilters = " ".join(new_tfilters) if new_tfilters else None

        _data.append({
            "name": tag,
            "enabled": enabled,
            "status": status,
            "url": url_for(endpoint=endpoint, in_request=in_request, page=page,
                mode=mode, search=search, filters=new_tfilters)
        })

    #
    _data = _data[:display_limit] if display_limit else _data

    tfilter = {
        "data": _data,
        "enabled": _enabled
    }

    return results, tfilter
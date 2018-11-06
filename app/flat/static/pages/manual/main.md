title: HLTS Manual
date: 2018-11-06

<!-- ![](/manual/static/images/sc1.png) -->

<a class="paddedAnchor" name="table-of-contents"></a>

# [Table of Contents](#table-of-contents)

- [Table of Contents](#table-of-contents)
    - [Annotations](#annotations)
        - [Editing Annotations](#editing-annotations)
        - [Tags and Collections](#tags-and-collections)
        - [Bulk Editing](#bulk-editing)
        - [Customizing Tags and Collections](#customizing-tags-and-collections)
    - [Searching Annotations](#searching-annotations)
        - [Search Syntax Examples](#search-syntax-examples)
        - [Search Syntaxes](#search-syntaxes)
    - [Using Markdown](#using-markdown)
    - [Backing up your data](#backing-up-your-data)
    - [Restoring Your Data](#restoring-your-data)
    - [API](#api)
        - [Your API Key](#your-api-key)
        - [Importing Annotations](#importing-annotations)
        - [API Requirements](#api-requirements)
        - [Annotation Schema](#annotation-schema)
        - [Annotation Schema Details](#annotation-schema-details)
        - [Example Annotation](#example-annotation)
        - [Example Connection Function](#example-connection-function)

<br>
***
<br>

<a class="paddedAnchor" name="annotations"></a>

## [Annotations](#annotations)

Each entry in HLTS is called an `Annotation` and each Annotation comes with six user-editable fields: `passage` `source` `author` `notes` `tags` and `collections`. The intention was to create a model with generic fields that would provide enough flexibility to enter and organize any sort of thought, idea or citation.

There are two ways to create an Annotation. Through the [New Annotation](/new) page or through the [API](/manual/main/#api).

<br>

<a class="paddedAnchor" name="editing-annotations"></a>

### [Editing Annotations](#editing-annotations)

==SECTION WIP==

<br>

<a class="paddedAnchor" name="tags-and-collections"></a>

### [Tags and Collections](#tags-and-collections)

All Annotations can have a set of `tags` and `collections`. Both are nearly identical in the way they are implemented under the hood and in the UI however in principle they serve two different functions. An Annotation's `tags` is a list of topics pertaining the content of the Annotation. They serve more as a "property" of the Annotation. Whereas an Annotation's `collections` are more to be considered as a bin that holds or connects different Annotations regardless of their tags.

<br>

<a class="paddedAnchor" name="bulk-editing"></a>

### [Bulk Editing](#bulk-editing-tags-and-collection)

The Annotation editor (see: [Editing Annotations](#editing-annotations)) allows users to add/edit/remove a single Tag/Collection/Source/Author however to edit all occurrences of a specific Tag/Collection/Source/Author, users can use a Bulk Editor. Accessible through the [Index](/index) page or by following one of these links: [Edit Tags](/edit/tags), [Edit Collections](/edit/collections), [Edit Sources](/edit/sources), [Edit Authors](/edit/authors)

> **WARNING:** Editing `Sources` and `Authors` is still very beta. Please be careful. There still isn't proper handling of duplicate/conflicting names.

<br>

<a class="paddedAnchor" name="customizing-tags-and-collections"></a>

### [Customizing Tags and Collections](#customizing-tags-and-collections)

All `Tags` and `Collections` can be edited and/or customized. Each comes with four customizable attributes: `name` `color` `description` `pinned`. These attributes are listen on the Bulk Editor pages. Accessible through the [Index](/index) page or by following one of these links: [Edit Tags](/edit/tags), [Edit Collections](/edit/collections).

The `pinned` attribute determines whether or not the Tag/Collection will appear on the [Dashboard](/dashboard). The `color` attribute can be set using any color syntax valid in CSS. e.g CSS Color Name, HEX, RGB and HSL. A color picker such as the one found here [htmlcolorcodes.com](https://htmlcolorcodes.com/color-picker/) can be used to choose a color and paste it into the `color` field.

<br>

Each of these color syntaxes is accepted and will produce the color red.

``` css
red               /* CSS Color Name */
#FF0000           /* HEX */
rgb(255, 0, 0)    /* RGB */
hsl(0, 100%, 50%) /* HSL */
```

<br>

For example:
<span class="pill tag examplePurplePill">yellow</span> <span class="pill tag exampleRedPill">green</span> <span class="pill tag exampleGreenPill">red</span> <span class="pill tag exampleYellowPill">purple</span>

Is represented by:

``` css
hsl(10, 100%, 80%) /* purple */
hsl(250, 85%, 85%) /* red */
hsl(130, 60%, 80%) /* green */
hsl(50, 100%, 70%) /* yellow */
```


<br>
***
<br>

<a class="paddedAnchor" name="searching-annotations"></a>

## [Searching Annotations](#searching-annotations)

HLTS comes with a custom text search syntax. Users are able to choose which field to search with a set of simple field keywords. e.g. `passage: {query}` to search `passages` or `tag: {query}` to search `tags`. In addition, users can use the keywords `and` `or` as booleans i.e. `art and creativity` to search for the two terms `art` and `creativity`. However, when wrapped in quotes i.e. `"art and creativity"` boolean key words are ignored and the search is conducted on the raw string. For more examples see: [Search Syntax Examples](#search-syntax-examples).

> **WARNING:** The query string parser is not very smart at the moment. Straying too far from the following recommended syntax will produce unexpected results.

<a class="paddedAnchor" name="search-syntax-examples"></a>

### [Search Syntax Examples](#syntax-examples)


`art`
Search for **art** in all fields.

> **NOTE:** Every query is a wrapped wildcard query. In other words, the query looks like this `*art*`. Therefore the query `art` will match to all occurrences of the string `art` whether it it's alone or inside of another word e.g. `artist` `heart` and `department`.

`passage: art`
Search for **art** only in passages.

`tags: art`
Search for **art** only in tags.

`art and creativity`
Search for **art** and **creativity** in all fields.

> **NOTE:** Boolean keywords are `and` and `or`. When added to a query, the first instance of either word with modify how the search is performed. Queries such as `art and or creativity` will return an error.

`art or creativity`
Search for **art** or **creativity** in all fields.

`"art and creativity"`
Search for the complete string **art and creativity** in all fields.

> **NOTE:** When boolean keywords appear inside in either single or double quotes they become part of an explicit search string. Therefore `"art and creativity"` will return only results that match the exact string.

`passage: art and creativity`
Search for **art** and **creativity** only in passages.

`tags: art and creativity`
Search for **art** and **creativity** only in tags.

<br>

<a class="paddedAnchor" name="search-syntaxes"></a>

### [Search Syntaxes](#search-syntaxes)

+ Syntax A : `[key]: {query}`
    + Passages
        + `p: {query}`
        + `passage: {query}`
        + `passages: {query}`
    + Sources
        + `s: {query}`
        + `source: {query}`
        + `sources: {query}`
        + `title: {query}`
    + Authors
        + `a: {query}`
        + `author: {query}`
        + `authors: {query}`
        + `by: {query}`
    + Tags
        + `t: {query}`
        + `tag: {query}`
        + `tags: {query}`
    + Collections
        + `c: {query}`
        + `collection: {query}`
        + `collections: {query}`
    + Notes
        + `n: {query}`
        + `note: {query}`
        + `notes: {query}`

<br>

+ Syntax B : `-[key] {query}`
    + Passages
        + `-p {query}`
        + `-passage {query}`
        + `-passages {query}`
    + Sources
        + `-s {query}`
        + `-source {query}`
        + `-sources {query}`
        + `-title {query}`
    + Authors
        + `-a {query}`
        + `-author {query}`
        + `-authors {query}`
        + `-by {query}`
    + Tags
        + `-t {query}`
        + `-tag {query}`
        + `-tags {query}`
    + Collections
        + `-c {query}`
        + `-collection {query}`
        + `-collections {query}`
    + Notes
        + `-n {query}`
        + `-note {query}`
        + `-notes {query}`

<br>
***
<br>

<a class="paddedAnchor" name="using-markdown"></a>

## [Using Markdown](#using-markdown)

see: [Using Markdown in HLTS](/manual/markdown)

<br>
***
<br>

<a class="paddedAnchor" name="backing-up-your-data"></a>

## [Backing up your data](#backing-up-your-data)

There are two options found on the [Tools](/tools) page for backing up your data `download` and `email`. Downloading will save it to your local disk whereas emailing will send the `.hlts` file to your currently set e-mail address. Both options generate an `.hlts` file containing all your data: annotations, tags, collections and their customized settings. In case of an emergency or a migration to another app, this file can be used to completely restore all your work.

<br>
***
<br>

<a class="paddedAnchor" name="restoring-your-data"></a>

## [Restoring Your Data](#restoring-your-data)

To restore your data go to the [Restore User Data](/restore_user_data) page (Also accessible through the [Tools](/tools) page). Click `Choose File` and select your latest `.hlts` file. Check the `Confirm` box and then press `Restore`.

The `.hlts` file will be validated to make sure the data is in the right format otherwise it will fail. In the case it fails please [Contact Us](/misc/contact).

> **NOTE:** Due to server and timeout limits, all Annotation imports are submitted as background jobs. Currently this poses a bit of a problem in that errors only show up in logs which are not very visible to the user. Future versions will have more interaction with background jobs.

**WARNING:** Restoring user data will **erase all your user settings and annotations** and replace them with what is found in the uploaded `.hlts` file. Please make sure to have a proper backup before proceeding.

<br>
***
<br>

<a class="paddedAnchor" name="api"></a>

## [API](#api)

HLTS provides simple API methods to import Annotations from an external application.
<br>

<a class="paddedAnchor" name="your-api-key"></a>

### [Your API Key](#your-api-key)

Users can access their API Key at the bottom of the [User Settings](/settings) page. The API Key is required to connect to your account with an external application. (see: [Example Connection Function](#example-connection-function))

<br>

<a class="paddedAnchor" name="importing-annotations"></a>

### [Importing Annotations](#importing-annotations)

The API provides two methods to import Annotations. An `add` method and a `refresh` method.

> **NOTE:** Due to server and timeout limits, all Annotation imports are submitted as background jobs. Currently this poses a bit of a problem in that errors only show up in logs which are not visible to the user. Future versions will have more interaction with background jobs.

+ **Add Annotations**
    + url: `api/async/import/annotations/add`
    + The `add` method adds a new annotation only if does not currently exist. If no `id` is provided a new Annotation will be added.

> **NOTE:** The only way to test if an Annotation exists is to check the Annotation's `id`. HLTS is unaware of the contents of an Annotation and will import an Annotation multiple times if it does not find an existing `id`.

+ **Refresh Annotations**
    + url: `api/async/import/annotations/refresh`
    + The `refresh` method deletes and re-adds an Annotation if exists but only if `protected=False`. The `protected` attribute is set to `True` when a new Annotation is added by the user. However, to make refreshing an Annotation possible, imported Annotations that have the potential to be refreshed can have their `protected` attribute set to `False`. This allows the `refresh` method to remove the annotation when it detects another one with the same `id` and replace it with the updated version.


<br>

<a class="paddedAnchor" name="api-requirements"></a>

### [API Requirements](#api-requirements)

+ All requests should be made via the POST method.
+ Annotations should be submitted at a list of dictionaries following the [Annotation Schema](#annotation-schema).
+ When sending Annotations to the API, each dictionary in the list MUST match the [Annotation Schema](#annotation-schema). If any item is missing from the dictionary the import will fail.

<br>

<a class="paddedAnchor" name="annotation-schema"></a>

### [Annotation Schema](#annotation-schema)

Annotation JSON Schema

``` json
{
    "id": string,
    "passage": text,
    "notes": text,
    "source": {
        "name": text,
        "author": text
    },
    "tags": list,
    "collections": list,
    "created": date,
    "modified": date,
    "origin": string,
    "protected": bool,
    "deleted": bool
}
```

<br>

<a class="paddedAnchor" name="annotation-schema-details"></a>

### [Annotation Schema Details](#annotation-schema-details)

+ `id`
    + **required:** false
    + **input type:** string or `null`
    + **max:** 64
    + **default:** uuid4
    + **description:** If `null` a [uuid4](https://docs.python.org/2/library/uuid.html#uuid.uuid4) is generated.
+ `passage`
    + **required:** true
    + **input type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** n/a
+ `notes`
    + **required:** false
    + **input type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** n/a
+ `source:name`
    + **required:** false
    + **input type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** Provided text will create a `Source` object and set `Source.name` as `source:name` and `Source.author.name` as `source:author`
+ `source:author`
    + **required:** false
    + **input type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** Provided text will create a `Source` object and set `Source.author.name` as `source:author` and `Source.name` as `source:name`
+ `tags`
    + **required:** false
    + **input type:** list
    + **max:** n/a
    + **default:** n/a
    + **description:** If a `tag` in the list doesn't exist, a new `Tag` object will be created. Otherwise an existing `Tag` object will be linked to the Annotation.
+ `collections`
    + **required:** false
    + **input type:** list
    + **max:** n/a
    + **default:** n/a
    + **description:** If a `collection` in the list doesn't exist, a new `Collection` object will be created. Otherwise an existing `Collection` object will be linked to the Annotation.
+ `created`
    + **required:** false
    + **input type:** string as [ISO 8601 date](https://www.iso.org/iso-8601-date-and-time-format.html)
    + **max:** n/a
    + **default:** python `datetime` object
    + **description:** Provided [ISO 8601 date](https://www.iso.org/iso-8601-date-and-time-format.html) is converted to a python `datetime` object. Otherwise a new python `datetime` object is created at time of import.
+ `modified`
    + **required:** false
    + **input type:** string as [ISO 8601 date](https://www.iso.org/iso-8601-date-and-time-format.html)
    + **max:** n/a
    + **default:** python `datetime` object
    + **description:** Provided [ISO 8601 date](https://www.iso.org/iso-8601-date-and-time-format.html) is converted to a python `datetime` object. Otherwise a new python `datetime` object is created at time of import.
+ `origin`
    + **required:** false
    + **input type:** string
    + **max:** 64
    + **default:** "user"
    + **description:** This field can be used to sort different types of imports. e.g. "user" would refer to a user-created annotation whereas "apple_books" would refer to an annotation imported from Apple Books.
+ `protected`
    + **required:** false
    + **input type:** boolean
    + **max:** n/a
    + **default:** true
    + **description:** Determines whether or not an Annotation can be deleted during the API `refresh` method.
+ `deleted`
    + **required:** false
    + **input type:** boolean
    + **max:** n/a
    + **default:** false
    + **description:** Soft delete attribute.

<br>

<a class="paddedAnchor" name="example-annotation"></a>

### [Example Annotation](#example-annotation)

A valid JSON Annotation.

``` json
[
    {
        "id": "33586B95-BEB9-4C00-809B-28D223705C3A",
        "passage": "We are not here to do what has already been done.",
        "notes": "",
        "source": {
            "author": "Robert Henri",
            "name": "The Art Spirit"
        },
        "tags": [
            "art",
            "creativity"
        ],
        "collections": [
            "star"
        ],
        "created": "2017-11-01T22:35:56.799645",
        "modified": "2017-12-10T22:31:31.432650",
        "origin": "ibooks",
        "protected": false,
        "deleted": false
    }
]
```

<br>

<a class="paddedAnchor" name="example-connection-function"></a>

### [Example Connection Function](#example-connection-function)

A simple API connection function in python3.

``` python
import requests
import json
from typing import List, Union

def api_connect(url: str, api_key: str, data: List[dict]) -> Union[bool, Exception]:

    data = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        r = requests.post(url, data=data, headers=headers)

        try:
            response = r.json()
            print(response)

        except json.decoder.JSONDecodeError:
            raise Exception("No response from server...")

    except requests.exceptions.ConnectionError as err:
        raise Exception("Connection Refused: The server is probably down...")

    else:
        return True
```
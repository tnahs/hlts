title: HLTS Manual
date: 2018-11-03

<!-- ![](/manual/static/images/sc1.png) -->

<a class="paddedAnchor" name="table-of-contents"></a>

# Table of Contents

- [Table of Contents](#table-of-contents)
    - [Annotations](#annotations)
        - [Tags and Collections](#tags-and-collections)
        - [Customizing Tags and Collections](#customizing-tags-and-collections)
        - [Bulk Editing Sources and Authors](#bulk-editing-sources-and-authors)
    - [Searching Annotations](#searching-annotations)
        - [Examples](#examples)
        - [Syntaxes](#syntaxes)
    - [Using Markdown](#using-markdown)
    - [Backing up your data](#backing-up-your-data)
    - [Restoring Your Data](#restoring-your-data)
    - [API](#api)
        - [Your API Key](#your-api-key)
        - [Importing Annotations](#importing-annotations)
        - [API Requirements](#api-requirements)
        - [Annotation Schema](#annotation-schema)
        - [Example Connection Function](#example-connection-function)

<br>
***
<br>

<a class="paddedAnchor" name="annotations"></a>

## Annotations

Each entry in HLTS is called an `Annotation` and each Annotation comes with six user-editable fields: `passage` `source` `author` `notes` `tags` and `collections`. The intention was to create a model with generic fields that would provide enough flexibility to enter and organize any sort of thought, idea or citation.

There are two ways to create an Annotation. Through the [New Annotation](/new) page or through the [API](/manual/main/#api).

<br>

<a class="paddedAnchor" name="tags-and-collections"></a>

### Tags and Collections

All annotations can have a set of `tags` and `collections`. Both are nearly identical in the way they are implemented under the hood and in the UI however in principle they serve two different functions. An Annotation's `tags` is a list of topics pertaining the content of the Annotation. They serve more as a "property" of the Annotation. Whereas an Annotation's `collections` are more to be considered as a bin that holds or connects different Annotations regardless of their tags.

<br>

<a class="paddedAnchor" name="customizing-tags-and-collections"></a>

### Customizing Tags and Collections

<span class="pill tag examplePurplePill">example-tag1</span> <span class="pill tag exampleRedPill">example-tag2</span> <span class="pill tag exampleBluePill">example-tag3</span>

==SECTION WIP==

<br>

<a class="paddedAnchor" name="bulk-editing-sources-and-authors"></a>

### Bulk Editing Sources and Authors

==SECTION WIP==

<br>
***
<br>

<a class="paddedAnchor" name="searching-annotations"></a>

## Searching Annotations

==SECTION WIP==

**WARNING:** The query string parser is not very smart at the moment. Straying too far from the following recommended syntax will produce unexpected results.

<br>

<a class="paddedAnchor" name="examples"></a>

### Examples

`art`
Search for **art** in all fields.

> **NOTE:** Every query is a wrapped wildcard query. In other words, the query looks like this `*art*`. Therefore the query `art` will match to all occurances of the string `art` whether it it's alone or inside of another word i.e. artist, heart and department.

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
Search for **love** and **creativity** only in tags.

<br>

<a class="paddedAnchor" name="syntaxes"></a>

### Syntaxes

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

## Using Markdown

see: [Using Markdown in HLTS](/manual/markdown)

<br>
***
<br>

<a class="paddedAnchor" name="backing-up-your-data"></a>

## Backing up your data

There are two options found on the [Tools](/tools) page for backing up your data `download` and `email`. Downloading will save it to your local disk whereas emailing will send the `.hlts` file to your currently set e-mail address. Both options generate an `.hlts` file containing all your data: annotations, tags, collections and their customized settings. In case of an emergency or a migration to another app, this file can be used to completely restore all your work.

<br>
***
<br>

<a class="paddedAnchor" name="restoring-your-data"></a>

## Restoring Your Data

To restore your data go to the [Restore User Data](/restore_user_data) page (Also accessible through the [Tools](/tools) page). Click `Choose File` and select your latest `.hlts` file. Check the `Confirm` box and then press `Restore`.

The `.hlts` file will be validated to make sure the data is in the right format otherwise it will fail. In the case it fails please [Contact Us](/manual/contact).

> **NOTE:** Due to server and timeout limits, all Annotation imports are submitted as background jobs. Currently this poses a bit of a problem in that errors only show up in logs which are not very visible to the user. Future versions will have more interaction with background jobs.

**WARNING:** Restoring user data will **erase all your user settings and annotations** and replace them with what is found in the uploaded `.hlts` file. Please make sure to have a proper backup before proceeding.

<br>
***
<br>

<a class="paddedAnchor" name="api"></a>

## API

HLTS provides simple API methods to import Annotations from an external application. Currently only importing and simple querying are supported.

<br>

<a class="paddedAnchor" name="your-api-key"></a>

### Your API Key

Every user comes with an API Key found at the bottom of the [User Settings](/settings) page. The API Key is required to connect to your account with an external application.

<br>

<a class="paddedAnchor" name="importing-annotations"></a>

### Importing Annotations

The API provides two methods to import Annotations. An `add` method and a `refresh` method.

> **NOTE:** Due to server and timeout limits, all Annotation imports are submitted as background jobs. Currently this poses a bit of a problem in that errors only show up in logs which are not very visible to the user. Future versions will have more interaction with background jobs.

+ **Add Annotations**
    + `api/async/import/annotations/add`
    + The `add` method adds a new annotation only if does not currently exist. If no `id` is provided a new Annotation will be added.

> **NOTE:** The only way to test if an Annotation exists is to check the Annotation's `id`. HLTS is unaware of the contents of an Annotation and will import an Annotation multiple times if it does not find an existing `id`.

+ **Refresh Annotations**
    + `api/async/import/annotations/refresh`
    + The `refresh` method deletes and re-adds an Annotation if exists but only if `protected=False`. The `protected` attribute is set to `True` when a new Annotation is added by the user. However, to make refreshing an Annotation possible, imported Annotations that have the potential to be refreshed can have their `protected` attribute set to `False`. This allows the `refresh` method to remove the annotation when it detects another one with the same `id` and replace it with the updated version.


<br>

<a class="paddedAnchor" name="api-requirements"></a>

### API Requirements

+ All requests should be made via the POST method.
+ Annotations should be submitted at a list of dictionaries.
+ When sending Annotations to the API, each dictionary in the list MUST match the [Annotation Schema](#annotation-schema). If any item is missing from the dictionary the import will fail.

<br>

<a class="paddedAnchor" name="annotation-schema"></a>

### Annotation Schema

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

+ `id`
    + **required:** false
    + **type:** string
    + **max:** 64
    + **default:** uuid4
    + **description:** If no `id` is provided a uuid4 will be generated.
+ `passage`
    + **required:** true
    + **type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** n/a
+ `notes`
    + **required:** false
    + **type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** n/a
+ `source:name`
    + **required:** false
    + **type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** Provided text will create a `Source` object and set `Source.name` as `source:name` and `Source.author.name` as `source:author`
+ `source:author`
    + **required:** false
    + **type:** text
    + **max:** n/a
    + **default:** n/a
    + **description:** Provided text will create a `Source` object and set `Source.author.name` as `source:author` and `Source.name` as `source:name`
+ `tags`
    + **required:** false
    + **type:** list
    + **max:** n/a
    + **default:** n/a
    + **description:** If a `tag` in the list doesn't exist, a new `Tag` object will be created. Otherwise an existing `Tag` object will be linked to the Annotation.
+ `collections`
    + **required:** false
    + **type:** list
    + **max:** n/a
    + **default:** n/a
    + **description:** If a `collection` in the list doesn't exist, a new `Collection` object will be created. Otherwise an existing `Collection` object will be linked to the Annotation.
+ `created`
    + **required:** false
    + **type:** iso8601 date
    + **max:** n/a
    + **default:** python `datetime` object
    + **description:** Provided date is converted to a python `datetime` object. Otherwise a new python `datetime` object is created at time of import.
+ `modified`
    + **required:** false
    + **type:** iso8601 date
    + **max:** n/a
    + **default:** python `datetime` object
    + **description:** Provided date is converted to a python `datetime` object. Otherwise a new python `datetime` object is created at time of import.
+ `origin`
    + **required:** false
    + **type:** string
    + **max:** 64
    + **default:** "user"
    + **description:** This field can be used to sort different types of imports. i.e. "user" would refer to a user-created annotation whereas "ibooks" would refer to an annotation imported from iBooks.
+ `protected`
    + **required:** false
    + **type:** boolean
    + **max:** n/a
    + **default:** true
    + **description:** Determines whether or not an Annotation can be deleted during the API `refresh` method.
+ `deleted`
    + **required:** false
    + **type:** boolean
    + **max:** n/a
    + **default:** false
    + **description:** Soft delete attribute.

<br>

Example Annotation

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

### Example Connection Function

A simple API connection function in python3.

``` python
import requests
import json
from typing import List, Union

def api_import(api_key: str, url: str, data: List[dict]) -> Union[bool, Exception]:

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
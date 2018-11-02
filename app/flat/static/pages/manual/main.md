title: Manual
date: 2018-10-23

<!-- ![](/manual/static/images/sc1.png) -->

<a class="paddedAnchor" name="table-of-contents"></a>

# Table of Contents

- [Table of Contents](#table-of-contents)
    - [Creating Annotations](#creating-annotations)
    - [Deleting Annotations](#deleting-annotations)
    - [Tags and Collections](#tags-and-collections)
    - [Searching Annotations](#searching-annotations)
        - [Examples](#examples)
        - [Syntaxes](#syntaxes)
    - [Using Markdown](#using-markdown)

<br>

<a class="paddedAnchor" name="creating-annotations"></a>

## Creating Annotations

Etiam ut justo at tellus laoreet mollis. Quisque mattis sed urna at maximus. Vivamus tempus, libero id viverra facilisis, massa nunc vulputate dolor, in mattis nulla velit eu mauris. Donec cursus et augue eget molestie. Quisque in justo quam. Phasellus non felis est. Aenean dui elit, fermentum condimentum placerat nec, eleifend sed ex.

<br>

<a class="paddedAnchor" name="deleting-annotations"></a>

## Deleting Annotations

Vivamus tempus, libero id viverra facilisis, massa nunc vulputate dolor, in mattis nulla velit eu mauris. Donec cursus et augue eget molestie. Quisque in justo quam. Phasellus non felis est. Aenean dui elit, fermentum condimentum placerat nec, eleifend sed ex.

<br>

<a class="paddedAnchor" name="tags-and-collections"></a>

## Tags and Collections

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam iaculis semper ipsum vitae semper. Maecenas quis elementum ipsum, ut rutrum tortor. In tellus ante, viverra sed bibendum sit amet, mattis at odio. Proin pulvinar, justo sit amet rhoncus venenatis, turpis purus efficitur lacus, et pharetra est elit non nisl. Etiam ut justo at tellus laoreet mollis. Quisque mattis sed urna at maximus. Vivamus tempus, libero id viverra facilisis, massa nunc vulputate dolor, in mattis nulla velit eu mauris. Donec cursus et augue eget molestie. Quisque in justo quam. Phasellus non felis est. Aenean dui elit, fermentum condimentum placerat nec, eleifend sed ex.

<br>

<a class="paddedAnchor" name="searching-annotations"></a>

## Searching Annotations

Ut fermentum, leo ac laoreet ultrices, tortor elit sagittis ante, at sagittis mi purus et lectus. Suspendisse quis ultricies nulla. Ut consequat justo facilisis, scelerisque augue in, ullamcorper felis. Cras fringilla dapibus neque at laoreet. Nullam ex diam, tempor nec ligula quis, aliquam dapibus tortor. Proin in neque nibh. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam in elit ac velit ullamcorper gravida a ac urna. Duis ut nulla dolor. Donec non nisi ultricies, euismod sem quis, vulputate felis. Aenean porttitor risus quis sem tincidunt, a lobortis arcu condimentum. Pellentesque fringilla, justo ut tempus venenatis, ex est placerat dui, sed scelerisque tellus dui ut libero. Nam ac vestibulum arcu.

> Warning: The query string parser is not very smart at the moment. Straying too far from the following recommended syntax might produce bizarre results.

<a class="paddedAnchor" name="examples"></a>

### Examples

`art`
Search for **art** in all fields.

> Note: Every query is a wrapped wildcard query. Meaning theoretcally the query looks like this `*art*` Therefore the query `art` will match to all occurances of the string `art` whether it it's alone or inside of another word i.e. artist, department.

`passage: art`
Search for **art** only in passages.

`tags: art`
Search for **art** only in tags.

`art and creativity`
Search for **art** and **creativity** in all fields.


`art or creativity`
Search for **art** or **creativity** in all fields.

`"art and creativity"`
Search for the complete string **art and creativity** in all fields.

> Note: Boolean keywords are `and` and `or`. When added to a query the first instance of either word with modify how the search is performed. Queries such as `art and or creativity` will return an error. However when inside in either single or double quotes they become part of an explicit search string. Therefore `"art and creativity"` will return only results that match the exact string.

`passage: art and creativity`
Search for **art** and **creativity** only in passages.

`tags: art and creativity`
Search for **love** and **creativity** only in tags.

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

<a class="paddedAnchor" name="using-markdown"></a>
## Using Markdown

Duis ut nulla dolor. Donec non nisi ultricies, euismod sem quis, vulputate felis. Aenean porttitor risus quis sem tincidunt, a lobortis arcu condimentum.

see: [Using Markdown in HLTS](/manual/markdown)
title: HLTS Beta Notes
date: 2018-11-06

<a class="paddedAnchor" name="table-of-contents"></a>

# [Table of Contents](#table-of-contents)

- [Table of Contents](#table-of-contents)
    - [Beta Welcome](#beta-welcome)
    - [Beta Questions](#beta-questions)
    - [Known Issues](#known-issues)
    - [Changelog](#changelog)
    - [Reporting Bugs](#reporting-bugs)
    - [Submitting Feature Suggestions](#submitting-feature-suggestions)

<br>

<a class="paddedAnchor" name="beta-welcome"></a>

## [Beta Welcome](#beta-welcome)

see: [Welcome to the HLTS Beta!](/beta/welcome)

<br>

<a class="paddedAnchor" name="beta-questions"></a>

## [Beta Questions](#beta-questions)

While designing HLTS these are some questions we've come across. Have a thought or a response to one of them? [Contact Us!](/misc/contact) As more questions come up this section will be updated.

<br>

+ Are the Annotation fields `passage` `source` `author` `notes` `tags` and `collections` enough for entering and organizing Annotations?
+ Should Collections/Tags/Sources/Authors auto-remove themselves when they are un-used? or should there be an option to remove the un-used ones?
+ Is Markdown useful and if so, should it be toggled per annotation or for app as a whole?
+ Should the "Recent" page be populated by annotations from the past **number of days** taken from user settings or just a list of annotations arranged by recently created date?

<br>

<a class="paddedAnchor" name="known-issues"></a>

## [Known Issues](#known-issues)

Some current quirks to note while using HLTS. None of these should cause any errors in functionality or loss of data. Found something not listed here? [Contact Us!](/misc/contact)

<br>

+ Dashboard Annotation count includes items in trash.
+ "Quote of the day" and "Topic of the day" may change when theres a change in the database.
+ Annotation counts on Index pages (Collections/Tags/Sources/Authors) include items in trash.
+ Index does not list Annotations that have no `source` or `author`.
+ When using Markdown and performing a search, `this passage` does not match `this ==passage==`.
+ Typing in the textarea in the Annotation Add/Edit page resets the scroll position of the page on input (keypress inside the textarea) when there's lots of text in editor.
+ Bulk Collection/Tag/Source/Author editor displays all items as "pinned" after single item is submitted. Hard refresh is required to show correct properties.
+ Searching certain odd strings such as `P : word` does some funky stuff with text highlighting the matches.
+ If Tag or Collection name does not start with a letter or number it will not appear on the Index page.
+ After an Annotation is trashed/restored/deleted or the trash emptied, the page Annotation count will be wrong.
+ Whenever entering Tags or Collections on Annotation Add/Edit page, there is a slight delay while data is fetched. This will be fixed in later versions.
+ The [Random Annotation/Tag](/random/default) page is very beta and not very interactive at the moment.
+ All the [Bulk Editing](/manual/main/#bulk-editing) pages are very beta. Please be careful. There still isn't proper handling of duplicate/conflicting names.


<br>

<a class="paddedAnchor" name="changelog"></a>

## [Changelog](#changelog)

+ **Main App**
    + v1.0.0beta - 2018-11-07
        + Initial Release

<br>

+ **Database Model**
    + v1.0.0beta - 2018-11-07
        + Initial Release
    + v1.1.0beta - 2018-12-20
        + `deleted` renamed to `in_trash`.
        + `protected` renamed to `is_protected`.
        + `api_key` string length reduced to 32 characters.

<br>

<a class="paddedAnchor" name="reporting-bugs"></a>

## [Reporting Bugs](#reporting-bugs)

Found a bug? [Contact Us!](/misc/contact)

<br>

<a class="paddedAnchor" name="submitting-feature-suggestions"></a>

## [Submitting Feature Suggestions](#submitting-feature-suggestions)

Have a feature suggestion? [Contact Us!](/misc/contact)
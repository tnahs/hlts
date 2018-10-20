# HLTS Manual

<div class="text upper faded">last updated october 20, 2018</div>

<br>

### Table of contents
1. [Tags and Collections](#tags-and-collections)
2. [Searching Annotations](#searching-annotations)
3. [Using Markdown](#using-markdown)
4. [Known Bugs](#known-bugs)
5. [Beta Questions](#beta-questions)

<br>

#### Tags and Collections <a name="tags-and-collections"></a>

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam iaculis semper ipsum vitae semper. Maecenas quis elementum ipsum, ut rutrum tortor. In tellus ante, viverra sed bibendum sit amet, mattis at odio. Proin pulvinar, justo sit amet rhoncus venenatis, turpis purus efficitur lacus, et pharetra est elit non nisl. Etiam ut justo at tellus laoreet mollis. Quisque mattis sed urna at maximus. Vivamus tempus, libero id viverra facilisis, massa nunc vulputate dolor, in mattis nulla velit eu mauris. Donec cursus et augue eget molestie. Quisque in justo quam. Phasellus non felis est. Aenean dui elit, fermentum condimentum placerat nec, eleifend sed ex.

<br>

#### Searching Annotations <a name="searching-annotations"></a>

Ut fermentum, leo ac laoreet ultrices, tortor elit sagittis ante, at sagittis mi purus et lectus. Suspendisse quis ultricies nulla. Ut consequat justo facilisis, scelerisque augue in, ullamcorper felis. Cras fringilla dapibus neque at laoreet. Nullam ex diam, tempor nec ligula quis, aliquam dapibus tortor. Proin in neque nibh. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam in elit ac velit ullamcorper gravida a ac urna. Duis ut nulla dolor. Donec non nisi ultricies, euismod sem quis, vulputate felis. Aenean porttitor risus quis sem tincidunt, a lobortis arcu condimentum. Pellentesque fringilla, justo ut tempus venenatis, ex est placerat dui, sed scelerisque tellus dui ut libero. Nam ac vestibulum arcu.

<br>

#### Using Markdown <a name="using-markdown"></a>

see: <a href="markdown">Using Markdown in HLTS</a>

<br>

#### Known Bugs <a name="known-bugs"></a>

1. Dashboard annotation count includes deleted items.
2. Annotation counts on Index pages (Collections/Tags/Sources/Authors) include deleted items.
3. Index does not list annotations that have no `source` or `author`.
4. When using markdown and making a search, `this passage` does not match `this ==passage==`.
5. Searching `source:` and/or `author:` requires placing wildcards `*` around the query otherwise it looks for exact matches.
6. Annotation editor texarea resets the scroll position of the page on input (keypress inside the textarea) when there's lots of text in editor.
7. Bulk Collection/Tag/Source/Author editor displays all items as "pinned" after single item is submitted. Hard refresh is required to show correct properties.
8. Searching certain odd strings such as `P : word` does some funky stuff with text highlighting the matches.

<br>

#### Beta Questions <a name="beta-questions"></a>

List of questions!

1. Should Collections/Tags/Sources/Authors auto-remove themselves when they are un-used? or should we have a function to remove the un-used ones?
2. Is Markdown useful and if so, should it be toggled per annotation or for app as a whole?
3. Should the "Recent" page be past _n_ days taken from user settings or just a list of annotations arranged by recently created date?
title: Bugs
date: 2018-10-23

Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam in elit ac velit ullamcorper gravida a ac urna. Duis ut nulla dolor. Donec non nisi ultricies, euismod sem quis, vulputate felis. Aenean porttitor risus quis sem tincidunt, a lobortis arcu condimentum.

<br>

1. Dashboard annotation count includes deleted items.
2. Annotation counts on Index pages (Collections/Tags/Sources/Authors) include deleted items.
3. Index does not list annotations that have no `source` or `author`.
4. When using markdown and making a search, `this passage` does not match `this ==passage==`.
5. Searching `source:` and/or `author:` requires placing wildcards `*` around the query otherwise it looks for exact matches.
6. Annotation editor texarea resets the scroll position of the page on input (keypress inside the textarea) when there's lots of text in editor.
7. Bulk Collection/Tag/Source/Author editor displays all items as "pinned" after single item is submitted. Hard refresh is required to show correct properties.
8. Searching certain odd strings such as `P : word` does some funky stuff with text highlighting the matches.
title: How to use Markdown
date: 2018-11-06

<a class="paddedAnchor" name="table-of-contents"></a>

# Table of Contents

- [Table of Contents](#table-of-contents)
    - [Text styling](#text-styling)
    - [Lists](#lists)
    - [Misc Elements](#misc-elements)

<br>

HLTS comes pre-packaged with the ability to render Markdown. The following examples are the basics of how to use Markdown in HLTS as there are a few things specific to HLTS. The intent is to add some rich text formatting without resorting to HTML. Markdown adds a few very simple methods to **bold**  *italicize* _underline_ and ==highlight== text while also providing more complex methods to format text if necessary. Most Annotations with not find themselves filled with complex Markdown but just these few simple modes of emphasis to highlight specifics within an Annotation.

via. [Markdown Documentation](https://daringfireball.net/projects/markdown/syntax):

>Markdown's syntax is intended for one purpose: to be used as a format for *writing* for the web.

>Markdown is not a replacement for HTML, or even close to it. Its syntax is very small, corresponding only to a very small subset of HTML tags. The idea is *not* to create a syntax that makes it easier to insert HTML tags. In my opinion, HTML tags are already easy to insert. The idea for Markdown is to make it easy to read, write, and edit prose. HTML is a *publishing* format; Markdown is a *writing* format. Thus, Markdown's formatting syntax only addresses issues that can be conveyed in plain text.

>For any markup that is not covered by Markdown's syntax, you simply use HTML itself. There's no need to preface it or delimit it to indicate that you're switching from Markdown to HTML; you just use the tags.

<a class="paddedAnchor" name="text-styling"></a>

## [Text styling](#table-of-contents)

1. **bold** : `Ctrl/Cmd + b`
2. *italics* :  `Ctrl/Cmd + i`
3. _underline_ : `Ctrl/Cmd + u`
4. ~~strikethrough~~ : `Ctrl/Cmd + s`
5. ==highlight== : `Ctrl/Cmd + h`
6. Combined styles with ==**asterisks and equal signs**==.


Written as:

``` markdown
## [Text styling](#table-of-contents)

1. **bold** : `Ctrl/Cmd + b`
2. *italics* :  `Ctrl/Cmd + i`
3. _underline_ : `Ctrl/Cmd + u`
4. ~~strikethrough~~ : `Ctrl/Cmd + s`
5. ==highlight== : `Ctrl/Cmd + h`
6. Combined styles with ==**asterisks and equal signs**==.
```

<br>

<a class="paddedAnchor" name="lists"></a>

## [Lists](#table-of-contents)

1. Ordered list item
2. Another item
    * Unordered sub-list
        * Unordered list can use asterisks
        - Or minuses
        + Or pluses


Written as:

``` markdown
## [Lists](#table-of-contents)

1. Ordered list item
2. Another item
    * Unordered sub-list
        * Unordered list can use asterisks
        - Or minuses
        + Or pluses
```

<br>

<a class="paddedAnchor" name="misc-elements"></a>

## [Misc Elements](#table-of-contents)

> ==A block indented paragraph!== Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget nibh rutrum, semper quam sit amet, congue elit. Cras vulputate massa faucibus libero convallis vulputate. Proin quis pulvinar ipsum, eget luctus quam. Vestibulum pharetra fermentum turpis at luctus. Etiam sit amet enim non lorem interdum cursus. Vivamus vel pharetra mauris, vitae vehicula odio. Nullam auctor sapien et risus molestie, vel varius arcu mattis. Cras ac condimentum orci. ==Followed by a forced line break...==

<br>

==Next a regular paragraph...== Vivamus quam ligula, interdum ut pellentesque egestas, consectetur at arcu. Fusce placerat finibus ultricies. Proin quis semper metus. Quisque ut convallis nunc, non viverra ipsum. Sed rhoncus ex a enim elementum porttitor. ==...And then a horizontal rule.==

***


Written as:

``` markdown
## [Misc Elements](#table-of-contents)

> ==A block indented paragraph!== Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget nibh rutrum, semper quam sit amet, congue elit. Cras vulputate massa faucibus libero convallis vulputate. Proin quis pulvinar ipsum, eget luctus quam. Vestibulum pharetra fermentum turpis at luctus. Etiam sit amet enim non lorem interdum cursus. Vivamus vel pharetra mauris, vitae vehicula odio. Nullam auctor sapien et risus molestie, vel varius arcu mattis. Cras ac condimentum orci. ==Followed by a forced line break...==

<br>

==Next a regular paragraph...== Vivamus quam ligula, interdum ut pellentesque egestas, consectetur at arcu. Fusce placerat finibus ultricies. Proin quis semper metus. Quisque ut convallis nunc, non viverra ipsum. Sed rhoncus ex a enim elementum porttitor. ==...And then a horizontal rule.==

***
```

<br>

For more information on Markdown...

[Markdown Documentation](https://daringfireball.net/projects/markdown/syntax)
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

# Using Markdown in HLTS

<br>

HLTS comes pre-packaged with the ability to render Markdown. The following examples are the basics of how to use Markdown in HLTS as there are a few things specific to HLTS. The intent is to add some rich text formatting without resorting to HTML. Markdown adds a few very simple methods to **bold** _italicise_ and ==highlight== text while also providing more complex methods to format text. Most Annotations with not find themselves filled with complex Markdown but just these few simple modes of emphasis to highlight specifics within an annotation.

>Markdown's syntax is intended for one purpose: to be used as a format for *writing* for the web.

>Markdown is not a replacement for HTML, or even close to it. Its syntax is very small, corresponding only to a very small subset of HTML tags. The idea is *not* to create a syntax that makes it easier to insert HTML tags. In my opinion, HTML tags are already easy to insert. The idea for Markdown is to make it easy to read, write, and edit prose. HTML is a *publishing* format; Markdown is a *writing* format. Thus, Markdown's formatting syntax only addresses issues that can be conveyed in plain text.

>For any markup that is not covered by Markdown's syntax, you simply use HTML itself. There's no need to preface it or delimit it to indicate that you're switching from Markdown to HTML; you just use the tags.

> via. <https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet>


#### Text styling

1. **bold** : `Ctrl/Cmd + b`
2. *italics* :  `Ctrl/Cmd + i`
3. _underline_ : `Ctrl/Cmd + u`
4. ~~strikethrough~~ : `Ctrl/Cmd + s`
5. ==highlight== : `Ctrl/Cmd + h`
6. Combined styles with ==**asterisks and equal signs**==.


Written as:

``` markdown
_Text styling_

1. **bold** : `Ctrl/Cmd + b`
2. *italics* :  `Ctrl/Cmd + i`
3. _underline_ : `Ctrl/Cmd + u`
4. ~~strikethrough~~ : `Ctrl/Cmd + s`
5. ==highlight== : `Ctrl/Cmd + h`
6. Combined styles with ==**asterisks and equal signs**==.
```

<br>

#### Ordered/Unordered Lists

1. Ordered list item
2. Another item
    * Unordered sub-list.
        * Unordered list can use asterisks
        - Or minuses
        + Or pluses


Written as:

``` markdown
_Ordered/Unordered Lists_

1. Ordered list item
2. Another item
    * Unordered sub-list.
        * Unordered list can use asterisks
        - Or minuses
        + Or pluses
```

<br>

#### Misc Elements

> ==A block indented paragraph!== Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget nibh rutrum, semper quam sit amet, congue elit. Cras vulputate massa faucibus libero convallis vulputate. Proin quis pulvinar ipsum, eget luctus quam. Vestibulum pharetra fermentum turpis at luctus. Etiam sit amet enim non lorem interdum cursus. Vivamus vel pharetra mauris, vitae vehicula odio. Nullam auctor sapien et risus molestie, vel varius arcu mattis. Cras ac condimentum orci. ==Followed by a forced line break...==

<br>

==A regular paragraph...== Vivamus quam ligula, interdum ut pellentesque egestas, consectetur at arcu. Fusce placerat finibus ultricies. Proin quis semper metus. Quisque ut convallis nunc, non viverra ipsum. Sed rhoncus ex a enim elementum porttitor. ==...And then a horizontal rule.==

***


Written as:

``` markdown
#### Misc Elements

> ==A block indented paragraph!== Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget nibh rutrum, semper quam sit amet, congue elit. Cras vulputate massa faucibus libero convallis vulputate. Proin quis pulvinar ipsum, eget luctus quam. Vestibulum pharetra fermentum turpis at luctus. Etiam sit amet enim non lorem interdum cursus. Vivamus vel pharetra mauris, vitae vehicula odio. Nullam auctor sapien et risus molestie, vel varius arcu mattis. Cras ac condimentum orci. ==Followed by a forced line break...==

<br>

==A regular paragraph...== Vivamus quam ligula, interdum ut pellentesque egestas, consectetur at arcu. Fusce placerat finibus ultricies. Proin quis semper metus. Quisque ut convallis nunc, non viverra ipsum. Sed rhoncus ex a enim elementum porttitor. ==...And then a horizontal rule.==

***
```

<br>

_For more information on Markdown..._

Markdown Documentation: <https://daringfireball.net/projects/markdown/syntax>

Markdown Cheatsheet: <https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet>

<br>

<div class="text upper faded">Last updated: October 20, 2018</div>
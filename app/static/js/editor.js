"use strict";

window.addEventListener('load', function(){

    /* --------------------------------------------------------------------- */

    autoExpandTextarea()

    function autoExpandTextarea() {

        const textareas = document.querySelectorAll("textarea")

        if (textareas) {

            expandAll(textareas)

            window.addEventListener("resize", ( ) => {

                expandAll(textareas)
            });

            function expandAll(textareas){

                for (let texarea of textareas) {

                    expand(event, texarea)
                }
            }

            for (let texarea of textareas){

                texarea.addEventListener("paste", expand)
                texarea.addEventListener("input", expand)
                texarea.addEventListener("keyup", expand)
            }

            function expand(event, element){

                element = element || event.target

                // First shrinks the textarea with "inherit" then expands it.
                element.style.height = "inherit"
                element.style.height = `${element.scrollHeight}px`
            }
        }
    }


    /* --------------------------------------------------------------------- */
    /* --------------------------------------------------------------------- */
    /* --------------------------------------------------------------------- */
    /* --------------------------------------------------------------------- */
    /* --------------------------------------------------------------------- */
    /* --------------------------------------------------------------------- */

    function wrapString(prefix, suffix, area = document.activeElement) {

        const selection_start = area.selectionStart;
        const selection_end = area.selectionEnd;

        const selected_text = area.value.substring(selection_start, selection_end);
        const wrapped_text = prefix + selected_text + suffix;

        area.value = area.value.substring(0, selection_start)
                   + wrapped_text
                   + area.value.substring(selection_end, area.value.length);

        area.selectionEnd = selection_end + prefix.length;
    }

    function deletePair(event, left, right, area = document.activeElement) {

        const cursor_location = area.selectionStart;

        const padded_start = area.selectionStart - left.length;
        const padded_end = area.selectionEnd + right.length;

        const cursor_left = area.value.substring(padded_start, area.selectionEnd);
        const cursor_right = area.value.substring(area.selectionStart, padded_end);

        if (cursor_left === left && cursor_right === right) {

            area.value = area.value.substring(0, padded_start)
                       + area.value.substring(padded_end, area.value.length);

            area.selectionEnd = cursor_location - left.length;

            event.preventDefault();
        }
    }

    function moveCursor(area=document.activeElement){

        area.selectionEnd++;
        area.selectionStart++;
    }

    /* ---------------------------- general keyboard modifications ----------------------------------- */

    document.addEventListener('keydown', generalKeyboardMods);

    // const textareas = document.querySelectorAll("textarea")
    // const inputs = document.querySelectorAll("input")

    function generalKeyboardMods(e) {

        let area = document.activeElement;
        let area_tag = area.tagName.toLowerCase();

        if (area_tag == "textarea" || area_tag == "input") {

            /* --------------------
            * Create character pairs
            *
            * Wrap selected string or add character pair if no selection.
            * If pair is closed, and next character is closing sibling
            * skip the keydown command and move cursor forward.
            * --------------------*/

            const cursor_right = area.value.substring(area.selectionStart, area.selectionEnd + 1);

            // (parentheses)
            // left parenthesis (
            if (e.shiftKey && e.which == 57) {

                wrapString('(', ')');

                e.preventDefault();
            }
            // right parenthesis )
            else if ((e.shiftKey && e.which == 48) && cursor_right == ")") {

                moveCursor();

                e.preventDefault();
            }

            // {curly braces}
            // left curly brace {
            if (e.shiftKey && e.which == 219) {

                wrapString('{', '}');

                e.preventDefault();
            }
            // right curly brace }
            else if ((e.shiftKey && e.which == 221) && cursor_right == "}") {

                moveCursor();

                e.preventDefault();
            }

            // [braces]
            // left brace [
            if (!e.shiftKey && e.which == 219) {

                wrapString('[', ']');

                e.preventDefault();
            }
            // right brace ]
            else if ((!e.shiftKey && e.which == 221) && cursor_right == "]") {

                moveCursor();

                e.preventDefault();
            }

            // "double quotes"
            if (e.shiftKey && e.which == 222) {

                if (cursor_right == '"') {

                    moveCursor();

                } else {

                    wrapString('"', '"');
                }

                e.preventDefault();
            }

            /* --------------------
            * DISABLED
            * // 'single quotes'
            * if (!e.shiftKey && e.which == 222) {
            *
            *   if (cursor_right == "'") {
            *
            *       moveCursor();
            *
            *   } else {
            *
            *       wrapString("'", "'");
            *   }
            *
            *   e.preventDefault();
            * }
            * -------------------- */

            // `backticks`
            if (!e.shiftKey && e.which == 192) {

                if (cursor_right == "`") {

                    moveCursor();

                } else {

                    wrapString('`', '`');
                }

                e.preventDefault();
            }

            /* --------------------
            * Delete character pairs
            *
            * If cursor is sourrounded by a character pair, delete pairs
            * -------------------- */

            // 'delete' key
            if (e.which == 8) {

                deletePair(e, "(",")")

                deletePair(e, "[","]")

                deletePair(e, "{","}")

                deletePair(e, '"','"')

                deletePair(e, "'","'")

                deletePair(e, "`","`")
            }
        }
    }

    /* ---------------------------- markdown keyboard modifications ----------------------------------- */

    // TODO add un-wrap text? if text is italicized then un-italicize it on second click.

    document.addEventListener('keydown', markdownKeyboardMods);

    function markdownKeyboardMods(e) {

        let area = document.activeElement;

        // Only use these in markdown rendered fields.
        if (area.classList.contains("enableMarkdown")){

            // ctrl/cmd + b
            if ((e.metaKey || e.ctrlKey) && e.which == 66) {

                // **bold**
                wrapString("**", "**", area);

                e.preventDefault();
            }
            // ctrl/cmd + i
            else if ((e.metaKey || e.ctrlKey) && e.which == 73) {

                // *italic*
                wrapString("*", "*", area);

                e.preventDefault();
            }
            // ctrl/cmd + u
            else if ((e.metaKey || e.ctrlKey) && e.which == 85) {

                // _underline_
                wrapString("_", "_", area);

                e.preventDefault();
            }
            // ctrl/cmd + h
            else if ((e.metaKey || e.ctrlKey) && e.which == 72) {

                // ==highlight==
                wrapString("==", "==", area);

                e.preventDefault();
            }
            // ctrl/cmd + s
            else if ((e.metaKey || e.ctrlKey) && e.which == 83) {

                // ~~strikethrough~~
                wrapString("~~", "~~", area);

                e.preventDefault();
            }

            // 'delete' key
            if (e.which == 8) {

                deletePair(e, "_","_")

                deletePair(e, "*","*")

                deletePair(e, "=","=")

                deletePair(e, "~","~")
            }
        }
    }

});

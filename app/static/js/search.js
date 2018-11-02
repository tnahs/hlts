"use strict";

window.addEventListener("load", function(){

    console.log(searchInfo)

    markPassages(searchInfo);

    function markPassages(searchInfo) {

        if (!searchInfo["unsafe"]) {

            if (searchInfo["key"] == "" || searchInfo["key"] == "passages") {

                const markedClass = "marked";

                const terms = searchInfo["terms"];
                const passages = document.querySelectorAll(".annotationPassage");

                for (let passage of passages) {

                    for (let term of terms) {

                        const termRegExp = new RegExp(term, "gi");
                        const thisMatch = "$&";

                        const markup = `<span class="${markedClass}">${thisMatch}</span>`;
                        const markedHTML = passage.innerHTML.replace(termRegExp, markup);

                        passage.innerHTML = markedHTML;
                    }
                }
            }
        }
    }

});

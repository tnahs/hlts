"use strict";

window.addEventListener("load", function(){

    const betaPromptHideButton = document.querySelector(".betaPromptHideButton");

    betaPromptHideButton.addEventListener("click", function() {

        betaPromptHide()
    });

    function betaPromptHide() {

        const betaPrompt = document.querySelector("#betaPrompt");

        fetch("/ajax/hide_beta_prompt", {
            method: "POST",
            credentials: "include"
        })
        .then((response) => {

            if (response.ok) {

                betaPrompt.remove();
            }

        })
        .catch((error) => {

            console.log(error);
        });
    }

});

"use strict";

window.addEventListener("load", function(){

    /* -------------------------------------------------------------------- */
    /* Close mainFlash ------------------------------------------------- */

    const mainFlashMessages = document.querySelectorAll("mainFlash .flashMessage");

    if (mainFlashMessages) {

        for (let mainFlashMessage of mainFlashMessages) {

            const flashClose = mainFlashMessage.querySelector(".flashClose");

            flashClose.addEventListener("click", function() {

                mainFlashMessage.remove()
            });
        }
    }

    /* -------------------------------------------------------------------- */
    // Nav ---------------------------------------------------------------- */

    navDropShadow()

    document.addEventListener("scroll", ( ) => {

        navDropShadow()
    });

    function navDropShadow() {

        const nav = document.querySelector("nav");

        if (window.scrollY > 0) {

            nav.classList.add("dropShadowBig");
        }
        else {

            nav.classList.remove("dropShadowBig");
        }
    }

    // create menu

    const iconCreateMenu = document.querySelector(".iconCreateMenu");
    const createMenuChoices = document.querySelector("#createMenuChoices");

    iconCreateMenu.addEventListener("click", function() {

        if (!createMenuChoices.style.display || createMenuChoices.style.display === "none") {

            iconCreateMenu.classList.add("iconCreateMenuActive");
            createMenuChoices.style.display = "block";
        }
        else {

            iconCreateMenu.classList.remove("iconCreateMenuActive");
            createMenuChoices.style.display = "none";
        }
    });

    document.addEventListener("click", function(event) {

        if (event.target != iconCreateMenu) {

            iconCreateMenu.classList.remove("iconCreateMenuActive");
            createMenuChoices.style.display = "none";
        }
    });

    // user menu

    const iconMainMenu = document.querySelector(".iconMainMenu");
    const mainMenuChoices = document.querySelector("#mainMenuChoices");

    iconMainMenu.addEventListener("click", function() {

        if (!mainMenuChoices.style.display || mainMenuChoices.style.display === "none") {

            iconMainMenu.classList.add("iconUserMenuActive");
            mainMenuChoices.style.display = "block";
        }
        else {

            iconMainMenu.classList.remove("iconUserMenuActive");
            mainMenuChoices.style.display = "none";
        }
    });

    document.addEventListener("click", function(event) {

        if (event.target != iconMainMenu) {

            iconMainMenu.classList.remove("iconUserMenuActive");
            mainMenuChoices.style.display = "none";
        }
    });

    // compact menu

    const iconMainMenuCompact = document.querySelector(".iconMainMenuCompact");
    const mainMenuCompactChoices = document.querySelector("#mainMenuCompactChoices");

    iconMainMenuCompact.addEventListener("click", function() {

        if (!mainMenuCompactChoices.style.display || mainMenuCompactChoices.style.display === "none") {

            iconMainMenuCompact.classList.add("iconMainMenuCompactActive");
            mainMenuCompactChoices.style.display = "block";
        }
        else {

            iconMainMenuCompact.classList.remove("iconMainMenuCompactActive");
            mainMenuCompactChoices.style.display = "none";
        }
    });

    document.addEventListener("click", function(event) {

        if (event.target != iconMainMenuCompact) {

            iconMainMenuCompact.classList.remove("iconMainMenuCompactActive");
            mainMenuCompactChoices.style.display = "none";
        }
    });


    //--------------------------------


    const toggleApiKey = document.querySelector("#toggleApiKey");
    const apiKey = document.querySelector("#apiKey");

    if(apiKey && toggleApiKey) {

        const blurredApiKey = "API KEY HIDDEN"

        apiKey.innerText = blurredApiKey;

        toggleApiKey.addEventListener("click", function() {

            if (apiKey.innerText === blurredApiKey) {

                apiKey.innerText = apiKey.getAttribute("value");
            }
            else {

                apiKey.innerText = blurredApiKey;
            }
        });
    }

    /* -------------------------------------------------------------------- */
    /* Color pills -------------------------------------------------------- */

    fetchColorsData("/ajax/colors");

    function fetchColorsData(pillColorsDataURL) {

        const pillColorsData = [];

        fetch(pillColorsDataURL, {credentials: "include"})
            .then(response => response.json())
            .then(data => {
                pillColorsData.push(...data);
                refreshPillColors(pillColorsData);
            }
        )
    }

    function refreshPillColors(pillColorsData) {

        const pills = document.querySelectorAll(".pill");

        for (let data of pillColorsData) {

            for (let pill of pills) {

                const pillName = pill.getAttribute("name");

                if (pillName == data.name){

                    pill.style.background = data.color;
                    pill.style.color = "white";
                }
            }
        }
    }
});


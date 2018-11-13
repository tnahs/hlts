"use strict";

window.addEventListener("load", function(){

    /* -------------------------------------------------------------------- */
    /* Close mainFlash ------------------------------------------------- */

    const flashMessages = document.querySelectorAll("mainFlash .flashMessage");

    if (flashMessages) {

        for (let flashMessage of flashMessages) {

            const flashClose = flashMessage.querySelector(".flashClose");

            flashClose.addEventListener("click", function() {

                flashMessage.remove()
            });
        }
    }

    /* -------------------------------------------------------------------- */
    // Nav ---------------------------------------------------------------- */


    document.addEventListener("scroll", ( ) => {

        let scrollY = window.scrollY;

        const nav = document.querySelector("nav");

        if (scrollY > 0) {

            nav.classList.add("dropShadowBig");
        }
        else {

            nav.classList.remove("dropShadowBig");
        }
    });

    // icon index

    const iconIndex = document.querySelector("#iconIndex");

    iconIndex.addEventListener("mouseover", function() {

        iconIndex.src = iconIndex.getAttribute("active");
    });

    iconIndex.addEventListener("mouseout", function() {

        iconIndex.src = iconIndex.getAttribute("inactive");
    });

    // icon recent

    const iconRecent = document.querySelector("#iconRecent");

    iconRecent.addEventListener("mouseover", function() {

        iconRecent.src = iconRecent.getAttribute("active");
    });

    iconRecent.addEventListener("mouseout", function() {

        iconRecent.src = iconRecent.getAttribute("inactive");
    });

    // icon create

    const iconCreateMenu = document.querySelector("#iconCreateMenu");
    const navCreateChoices = document.querySelector("#navCreateChoices");

    iconCreateMenu.addEventListener("mouseover", function() {

        iconCreateMenu.src = iconCreateMenu.getAttribute("active");
    });

    iconCreateMenu.addEventListener("mouseout", function() {

        if (!navCreateChoices.style.display || navCreateChoices.style.display === "none") {

            iconCreateMenu.src = iconCreateMenu.getAttribute("inactive");
        }
    });

    iconCreateMenu.addEventListener("click", function() {

        if (!navCreateChoices.style.display || navCreateChoices.style.display === "none") {

            iconCreateMenu.src = iconCreateMenu.getAttribute("active");
            navCreateChoices.style.display = "block";
        }
        else {

            iconCreateMenu.src = iconCreateMenu.getAttribute("inactive");
            navCreateChoices.style.display = "none";
        }
    });

    document.addEventListener("click", function(event) {

        if (event.target != iconCreateMenu) {

            iconCreateMenu.src = iconCreateMenu.getAttribute("inactive");
            navCreateChoices.style.display = "none";
        }
    });

    // icon trash

    const iconTrash = document.querySelector("#iconTrash");

    iconTrash.addEventListener("mouseover", function() {

        iconTrash.src = iconTrash.getAttribute("active");
    });

    iconTrash.addEventListener("mouseout", function() {

        iconTrash.src = iconTrash.getAttribute("inactive");
    });

    // icon user

    const iconUserMenu = document.querySelector("#iconUserMenu");
    const userMenuChoices = document.querySelector("#userMenuChoices");

    iconUserMenu.addEventListener("mouseover", function() {

        iconUserMenu.src = iconUserMenu.getAttribute("active");
    });

    iconUserMenu.addEventListener("mouseout", function() {

        if (!userMenuChoices.style.display || userMenuChoices.style.display === "none") {

            iconUserMenu.src = iconUserMenu.getAttribute("inactive");
        }
    });

    iconUserMenu.addEventListener("click", function() {

        if (!userMenuChoices.style.display || userMenuChoices.style.display === "none") {

            iconUserMenu.src = iconUserMenu.getAttribute("active");
            userMenuChoices.style.display = "block";
        }
        else {

            iconUserMenu.src = iconUserMenu.getAttribute("inactive");
            userMenuChoices.style.display = "none";
        }
    });

    document.addEventListener("click", function(event) {

        if (event.target != iconUserMenu) {

            iconUserMenu.src = iconUserMenu.getAttribute("inactive");
            userMenuChoices.style.display = "none";
        }
    });

    //--------------------------------


    const toggleAPIKey = document.querySelector("#toggleAPIKey");
    const apiKey = document.querySelector("#api_key");

    if(apiKey && toggleAPIKey) {

        apiKey.type = "password"

        toggleAPIKey.addEventListener("click", function() {

            if (apiKey.type === "password") {

                apiKey.type = "text";
            }
            else {

                apiKey.type = "password";
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

        const pills = document.querySelectorAll('.pill');

        for (let data of pillColorsData) {

            for (let pill of pills) {

                const pillName = pill.getAttribute('name');

                if (pillName == data.name){

                    pill.style.background = data.color;
                    pill.style.color = 'white';
                }
            }
        }
    }

    /* -------------------------------- show/hide annotation options -------------------------------- */

    const annotationContainersInteractive = document.querySelectorAll(".annotationContainerInteractive");

    for (let annotationContainer of annotationContainersInteractive) {

        annotationContainer.addEventListener("mouseover", function(){ activate(annotationContainer) });
        annotationContainer.addEventListener("mouseout", function(){ deactivate(annotationContainer) });
    }

    function activate(annotationContainer) {

        annotationContainer.classList.add("annotationContainerInteractiveVisible");
        annotationContainer.classList.add("dropShadowBig");

        const options = annotationContainer.lastElementChild;
        options.style.opacity = "1";
    }

    function deactivate(annotationContainer) {

        annotationContainer.classList.remove("annotationContainerInteractiveVisible");
        annotationContainer.classList.remove("dropShadowBig");

        const options = annotationContainer.lastElementChild;
        options.style.opacity = "0";
    }

});


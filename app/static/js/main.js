"use strict";

window.addEventListener("load", function(){

    /* -------------------------------------------------------------------- */
    /* Close mainFlash ------------------------------------------------- */

    const mainFlash = document.querySelector("mainFlash .flashContainer");

    if (mainFlash) {

        const main = document.querySelector("main");

        const rootStyles = window.getComputedStyle(document.body);
        const navMenuHeight = rootStyles.getPropertyValue("--nav-menu-height");
        const flashContainerHeight = rootStyles.getPropertyValue("--flash-container-height");
        const navMenuHeightInt = parseInt(navMenuHeight.slice(0, -2));
        const flashContainerHeightInt = parseInt(flashContainerHeight.slice(0, -2));

        main.style.paddingTop =  `${navMenuHeightInt + flashContainerHeightInt}px`;

        mainFlash.addEventListener("click", function() {

            mainFlash.remove()

            main.style.paddingTop = `${navMenuHeightInt}px`;
        });
    }

    const loginFlash = document.querySelector("loginFlash .flashContainer");

    if (loginFlash) {

        loginFlash.addEventListener("click", function() {

            loginFlash.remove()
        });
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


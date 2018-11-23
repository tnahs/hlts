"use strict";

window.addEventListener("load", function(){

    const betaNotificationHideButton = document.querySelector(".betaNotificationHideButton");

    betaNotificationHideButton.addEventListener("click", function() {

        betaNotificationHide()
    });

    function betaNotificationHide() {

        const betaNotification = document.querySelector("#betaNotification");

        fetch("/ajax/hide_beta_notification", {
            method: "POST",
            credentials: "include"
        })
        .then((response) => {

            if (response.ok) {

                betaNotification.remove();
            }

        })
        .catch((error) => {

            console.log(error);
        });
    }

});

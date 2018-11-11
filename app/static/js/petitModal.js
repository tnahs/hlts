"use strict";

class PetitModal {
    constructor ({
            closeIcon = "✕",
            cancelButtonText = "cancel",
            dialogBoxClasses = [],
            messageClasses = [],
            buttonClasses = [],
            warningClasses = [] } = {}) {

        this.defaultTriggerClass = "pmTrigger";

        this.closeIcon = closeIcon;
        this.cancelButtonText = cancelButtonText;
        this.defaultModalClass = "petitModal";
        this.defaultDialogBoxClass = "pmDialogBox";
        this.defaultMessageClass = "pmMessage";
        this.defaultCloseButtonClass = "pmClose";
        this.defaultCancelButtonClass = "pmCancel";
        this.defaultConfirmButtonClass = "pmConfirm";

        this.dialogBoxClasses = [this.defaultDialogBoxClass].concat(dialogBoxClasses).join(" ");
        this.messageClasses = [this.defaultMessageClass].concat(messageClasses).join(" ");
        this.closeButtonClasses = [this.defaultCloseButtonClass].concat(buttonClasses).join(" ");
        this.cancelButtonClasses = [this.defaultCancelButtonClass].concat(buttonClasses).join(" ");
        this.confirmButtonClasses = [this.defaultConfirmButtonClass].concat(buttonClasses).concat(warningClasses).join(" ");

        this.template = `
            <div class="${this.defaultModalClass}">
                <div class="${this.dialogBoxClasses}">
                    <div class="${this.messageClasses}"><!-- MESSAGE TEXT --></div>
                    <div class="${this.closeButtonClasses}">${this.closeIcon}</div>
                    <div class="${this.cancelButtonClasses}">${this.cancelButtonText}</div>
                    <div class="${this.confirmButtonClasses}"><!-- CONFIRM TEXT --></div>
                </div>
            </div>
            `;


        const body = document.querySelector("body");
        body.insertAdjacentHTML("beforeend", this.template);

        const petitModal = document.querySelector(`[class^="${this.defaultModalClass}"]`);
        const message = petitModal.querySelector(`[class^="${this.defaultMessageClass}"]`);
        const closeButton = petitModal.querySelector(`[class^="${this.defaultCloseButtonClass}"]`);
        const cancelButton = petitModal.querySelector(`[class^="${this.defaultCancelButtonClass}"]`);
        const confirmButton = petitModal.querySelector(`[class^="${this.defaultConfirmButtonClass}"]`);

        // Assemble PetitModal data
        this.petitModal = {
            main: petitModal,
            message: message,
            closeButton: closeButton,
            confirmButton: confirmButton,
            cancelButton: cancelButton
        }
    }

    initPetitModal() {

        this.petitModal.closeButton.addEventListener("click", ( ) => {

            this.hideModal();
        });

        this.petitModal.cancelButton.addEventListener("click", ( ) => {

            this.hideModal();
        });

        document.addEventListener("click", (event) => {

            this.windowClick(event);
        });

        //

        /* Creating pmTriggers
        *
        * <div class="pmTrigger" data="" message="" url="" action=""></div>
        *
        * */

        const pmTriggers = document.querySelectorAll(`[class*="${this.defaultTriggerClass}"]`);

        if (pmTriggers) {

            for (let pmTrigger of pmTriggers) {

                pmTrigger.addEventListener("click", ( ) => {

                    const data = pmTrigger.getAttribute("data");
                    const url = pmTrigger.getAttribute("url");
                    const message = pmTrigger.getAttribute("message");
                    const action = pmTrigger.getAttribute("action");

                    this.buildModal(data, url, message, action);

                });
            }
        }
    }

    buildModal(data, url, message, action) {

        const annotationElement = document.querySelector(`[id="${data}"]`);

        this.petitModal.message.innerText = `${message}`;
        this.petitModal.confirmButton.innerText = action;
        this.petitModal.confirmButton.addEventListener("click", ( ) => {

            this.submitModal(url, data, annotationElement);
        });

        document.addEventListener("keydown", (event) => {

            if (event.code == "Enter") {

                this.submitModal(url, data, annotationElement);

                event.preventDefault();
            }

            else if (event.code == "Escape") {

                this.hideModal();

                event.preventDefault();
            }
        });

        this.petitModal.main.style.opacity = 1;
        this.petitModal.main.style.visibility = "visible";
    }

    hideModal(){

        this.petitModal.main.style.opacity = 0;
        this.petitModal.main.style.visibility = "hidden";
    }

    submitModal(url, data, annotationElement) {

        // FIXMEMODAL

        fetch(url, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({id: data}),
        })
        .then((response) => {

            if (response.ok) {

                annotationElement.remove();
                this.hideModal();
            }

        })
        .catch((error) => {

            console.log(error);
        });

    }

    windowClick(event) {

        if (event.target === this.petitModal.main) {

            this.hideModal();
        }
    }
}

const myPetitModal = new PetitModal(
    {
        dialogBoxClasses: ["dropShadowBig"],
        messageClasses: ["text", "upper"],
        buttonClasses: ["link", "button"],
        warningClasses: ["warning"]
    }
)
myPetitModal.initPetitModal()
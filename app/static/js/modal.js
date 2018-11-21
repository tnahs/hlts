"use strict";

class Modal {
    constructor ({
            closeIcon = "✕",
            cancelButtonText = "cancel",
            confirmButtonText = "ok",
            dialogBoxClasses = [],
            messageClasses = [],
            buttonClasses = [],
            warningClasses = [] } = {}) {

        this.defaultTriggerClass = "modalTrigger";

        this.closeIcon = closeIcon;
        this.cancelButtonText = cancelButtonText;
        this.confirmButtonText = confirmButtonText;
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
                    <div class="${this.confirmButtonClasses}">${this.confirmButtonText}</div>
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

        // Assemble Modal attributes
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

        /* Creating modalTriggers
        *
        * <div class="modalTrigger" modalSubmitData="" modalConfirmMessage="" modalSubmitUrl="" modalAction=""></div>
        *
        * */

        const modalTriggers = document.querySelectorAll(`[class*="${this.defaultTriggerClass}"]`);

        if (modalTriggers) {

            for (let modalTrigger of modalTriggers) {

                modalTrigger.addEventListener("click", ( ) => {

                    const modalAction = modalTrigger.getAttribute("modalAction");
                    const modalSubmitData = modalTrigger.getAttribute("modalSubmitData");
                    const modalSubmitUrl = modalTrigger.getAttribute("modalSubmitUrl");
                    const modalConfirmMessage = modalTrigger.getAttribute("modalConfirmMessage");

                    this.buildModal(modalAction, modalSubmitData, modalSubmitUrl, modalConfirmMessage);

                });
            }
        }
    }

    buildModal(modalAction, modalSubmitData, modalSubmitUrl, modalConfirmMessage) {

        const annotationElement = document.querySelector(`[id="${modalSubmitData}"]`);

        this.petitModal.message.innerText = `${modalConfirmMessage}`;
        this.petitModal.confirmButton.addEventListener("click", ( ) => {

            this.submitModal(modalAction, modalSubmitUrl, modalSubmitData, annotationElement);
        });

        document.addEventListener("keydown", (event) => {

            if (event.code == "Enter") {

                this.submitModal(modalAction, modalSubmitUrl, modalSubmitData, annotationElement);

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

    submitModal(modalAction, modalSubmitUrl, modalSubmitData, annotationElement) {

        // FIXMEMODAL

        fetch(modalSubmitUrl, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({id: modalSubmitData}),
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

const myPetitModal = new Modal(
    {
        dialogBoxClasses: ["dropShadowBig"],
        messageClasses: ["text", "upper"],
        buttonClasses: ["link", "button"],
        warningClasses: ["warning"]
    }
)
// myPetitModal.initPetitModal()
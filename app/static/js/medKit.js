'use strict';

class MedKit {
    constructor (name,
        {
            pillCustomClasses = [],
            pillDataDelimiter = ' ', // can we use regex? also wanna add a way to protect this... so no spaces are ever submitted
            pillColorsData = [],
            pillColorsDataURL = false,
            pillBoxInputPlaceholder = '',
            suggestionsEnabled = true,
            suggestionLimit = 5,
            suggestionData = [],
            suggestionDataURL = false,
            validSubmitKeyCodes = ['Enter', 'Comma'],
            unsafeKeyCodes = ['Space'],
            unsafeKeyCodesReplacement = '-',
            zIndex = 0 } = {}) {

        this.name = name;

        this.dataId = `${name}-medKitData`;
        this.pillDefaultClass = ["medKitPill"];
        this.pillClasses = this.pillDefaultClass.concat(pillCustomClasses);
        this.pillBoxInputPlaceholder = pillBoxInputPlaceholder;
        this.pillDataDelimiter = pillDataDelimiter;

        this.pillBoxId = `${name}-medKitPillBox`;
        this.pillBoxInputId = `${name}-medKitInput`;
        this.pillColorsData = pillColorsData;
        this.pillColorsDataURL = pillColorsDataURL;

        this.suggestionBoxId = `${name}-medKitSuggestionBox`;
        this.suggestionClass = `${name}-medKitSuggestion`;
        this.suggestionSelectionId = `${name}-medKitSuggestionSelected`;
        this.suggestionsEnabled = suggestionsEnabled;
        this.suggestionData = suggestionData;
        this.suggestionDataURL = suggestionDataURL;
        this.suggestionLimit = suggestionLimit;
        this.suggestionsOpen = false;

        this.validSubmitKeyCodes = validSubmitKeyCodes;
        this.unsafeKeyCodes = unsafeKeyCodes;
        this.unsafeKeyCodesReplacement = unsafeKeyCodesReplacement;

        this.zIndex = zIndex;

        this.template = `
            <div id="${this.pillBoxId}">
                <!-- PILLS -->
                <input id="${this.pillBoxInputId}" type="text" placeholder="${this.pillBoxInputPlaceholder}">
                <div id="${this.suggestionBoxId}"><!-- SUGGESTIONS --></div>
            </div>
            `;

        // Fetch suggestion data
        if (this.suggestionDataURL && this.suggestionsEnabled) {

            fetch(this.suggestionDataURL, {credentials: 'include'})
                .then(response => response.json())
                .then(data => {
                    this.suggestionData.push(...data);
                    this.refreshSuggestions();
            });
        }

        // Fetch pill color data
        if (this.pillColorsDataURL) {

            fetch(this.pillColorsDataURL, {credentials: 'include'})
                .then(response => response.json())
                .then(data => {
                    this.pillColorsData.push(...data);
                    this.refreshPillColors();
            })
        }

        // Build Medkit HTML
        const main = document.querySelector(`medKit[name=${this.name}]`);

        main.innerHTML = this.template;

        const data = document.querySelector(`#${this.dataId}`)
        const pillBox = document.querySelector(`#${this.pillBoxId}`)
        const input = document.querySelector(`#${this.pillBoxInputId}`)
        const suggestionBox = document.querySelector(`#${this.suggestionBoxId}`)

        main.appendChild(data);

        if (this.zIndex) { main.style.zIndex = this.zIndex; }

        // Assemble Medkit data
        this.medKit = {
            pills: [],
            data: data,
            input: input,
            pillBox: pillBox,
            pillClasses: this.pillClasses,
            pillDataDelimiter: this.pillDataDelimiter,
            pillColorsData: this.pillColorsData,
            suggestionBox: suggestionBox,
            suggestionClass: this.suggestionClass,
            suggestionSelectionId: this.suggestionSelectionId,
            suggestionsEnabled: this.suggestionsEnabled,
            suggestionData: this.suggestionData,
            suggestionLimit: this.suggestionLimit,
            suggestionsOpen: this.suggestionsOpen,
            validSubmitKeyCodes: this.validSubmitKeyCodes,
            unsafeKeyCodes: this.unsafeKeyCodes,
            unsafeKeyCodesReplacement: this.unsafeKeyCodesReplacement
        }
    }

    initMedKit() {

        this.prefillPills();

        this.medKit.input.addEventListener('keydown', (event) => {

            this.mainInputHandler(event);
            this.arrowHandler(event)
        });

        this.medKit.input.addEventListener('input', ( ) => {

            this.refreshSuggestions();
        });

        document.addEventListener('click', ( ) => {

            this.clearAllWarnings();
            this.clearSuggestions();
            this.clearInput();
        });

        document.addEventListener('keyup', (event) => {

            if (event.code == 'Escape') {

                this.clearAllWarnings();
            }
        });
    }

    prefillPills() {

        const medKitData = this.medKit.data.value;

        if (medKitData) {

            let prefilledData = medKitData.split(this.medKit.pillDataDelimiter);

            this.medKit.data.value = '';

            for (let name of prefilledData) {

                this.createPill(name)
            }
        }
    }

    createPill(name) {

        const pill = {
            name: this.dataSafeName(name),
            button: document.createElement('div')
        };

        pill.button.textContent = `${pill.name}`;
        pill.button.classList.add(...this.medKit.pillClasses);
        pill.button.setAttribute('name', pill.name);
        pill.button.addEventListener('click', ( ) => {

            this.deletePill(pill);
            event.stopPropagation();
        });

        const medKitDataList = this.medKit.data.value.split(this.medKit.pillDataDelimiter);
        const newMedKitDataList = medKitDataList.concat(pill.name);

        this.medKit.data.value = newMedKitDataList.join(this.medKit.pillDataDelimiter);
        this.medKit.pillBox.insertBefore(pill.button, this.medKit.input);
        this.medKit.pills.push(pill)

        this.refreshPillColors()
    }

    deletePill(pill) {

        if (pill.button.classList.contains('warning')) {

            const medKitDataList = this.medKit.data.value.split(this.medKit.pillDataDelimiter);
            const newMedKitDataList = medKitDataList.filter(pillName => pillName !== pill.name);
            const pillIndex = this.medKit.pills.indexOf(pill)

            this.medKit.data.value = newMedKitDataList.join(this.medKit.pillDataDelimiter);
            this.medKit.pillBox.removeChild(pill.button);
            this.medKit.pills.splice(pillIndex, 1);
        }

        else {

            pill.button.classList.add('warning');
        }
    }

    refreshPillColors() {

        const pillClasses = this.medKit.pillClasses.map(cls => `.${cls}`).join(', ');
        const pills = document.querySelectorAll(pillClasses);

        for (let data of this.medKit.pillColorsData) {

            for (let pill of pills) {

                const pillName = pill.getAttribute('name');

                if (pillName == data.name){

                    pill.style.background = data.color;
                    pill.style.color = 'white';
                }
            }
        }
    }

    clearInput() {

        this.medKit.input.value = '';
    }

    mainInputHandler(event) {

        const medKitInputValue = this.medKit.input.value;
        const medKitPills = this.medKit.pills;

        if (this.medKit.validSubmitKeyCodes.includes(event.code)) {

            if (medKitInputValue.length != 0) {

                this.createPill(medKitInputValue);
                this.clearSuggestions();
                this.clearInput();
            }

            event.preventDefault();
        }

        else if (this.medKit.unsafeKeyCodes.includes(event.code)) {

            this.medKit.input.value += this.medKit.unsafeKeyCodesReplacement;

            event.preventDefault();
        }

        else if (event.code == 'Escape') {

            this.clearSuggestions();
            this.clearInput();
        }

        else if (event.code == 'Backspace') {

            if (medKitInputValue.length === 0 && medKitPills.length > 0) {

                this.deletePill(medKitPills[medKitPills.length-1])
            }
        }
    }

    arrowHandler(event) {

        if (this.medKit.suggestionsOpen) {

            const allSuggestions = this.medKit.suggestionBox.querySelectorAll(`.${this.suggestionClass}`);
            const firstSuggestion = allSuggestions[0];
            const lastSuggestion = allSuggestions[allSuggestions.length-1];

            const suggestionSelection = this.medKit.suggestionBox.querySelector(`#${this.medKit.suggestionSelectionId}`);

            if(event.code == 'ArrowDown') {

                if (suggestionSelection === null) {

                    firstSuggestion.id = this.medKit.suggestionSelectionId;
                    this.medKit.input.value = firstSuggestion.getAttribute('name')
                }

                else {

                    suggestionSelection.id = '';

                    const nextSuggestion = suggestionSelection.nextSibling;

                    if (nextSuggestion) {

                        nextSuggestion.id = this.medKit.suggestionSelectionId
                        this.medKit.input.value = nextSuggestion.getAttribute('name')
                    }
                }

                event.preventDefault();
            }

            if(event.code == 'ArrowUp') {

                if (suggestionSelection === null) {

                    lastSuggestion.id = this.medKit.suggestionSelectionId;
                    this.medKit.input.value = firstSuggestion.getAttribute('name')
                }

                else {

                    suggestionSelection.id = '';

                    const previousSuggesion = suggestionSelection.previousSibling;

                    if (previousSuggesion) {

                        previousSuggesion.id = this.medKit.suggestionSelectionId
                        this.medKit.input.value = previousSuggesion.getAttribute('name')
                    }
                }

                event.preventDefault();
            }
        }

        else {

            if(event.code == 'ArrowDown') {

                this.topSuggestions();
            }
        }
    }

    topSuggestions() {

        // TODO make DRY

        if (this.medKit.suggestionsEnabled) {

            this.clearSuggestions();

            this.medKit.suggestionsOpen = true;

            let suggestions = this.medKit.suggestionData;
            suggestions = suggestions.sort((a, b) => b.frequency - a.frequency)
            suggestions = suggestions.slice(0, this.medKit.suggestionLimit)

            for (let match of suggestions) {

                this.createSuggestion(match)
            }
        }
    }

    refreshSuggestions() {

        // TODO make DRY

        if (this.medKit.suggestionsEnabled) {

            this.clearSuggestions();

            const medKitInputValue = this.medKit.input.value;

            if (medKitInputValue) {

                this.medKit.suggestionsOpen = true;

                let suggestions = this.medKit.suggestionData;
                suggestions = this.filterSuggestions(suggestions, medKitInputValue);
                suggestions = suggestions.sort((a, b) => b.frequency - a.frequency)
                suggestions = suggestions.slice(0, this.medKit.suggestionLimit)

                for (let match of suggestions) {

                    this.createSuggestion(match)
                }
            }
        }
    }

    filterSuggestions(suggestions, input) {

        return suggestions.filter(item => {

            const regex = new RegExp(input, 'gi');

            return item.name.match(regex)
        });
    }

    createSuggestion(match) {

        let suggestion = {
            name: match.name,
            frequency: match.frequency,
            button: document.createElement('div')
        };

        suggestion.button.classList.add(this.medKit.suggestionClass);
        suggestion.button.setAttribute('name', suggestion.name);
        suggestion.button.textContent = `${suggestion.name} ⋅ ${suggestion.frequency}`;

        suggestion.button.addEventListener('click', ( ) => {

            this.createPill(suggestion.name)
            this.clearSuggestions();
            this.clearInput()
        });

        this.medKit.suggestionBox.appendChild(suggestion.button);
    }

    clearSuggestions() {
        this.medKit.suggestionBox.innerHTML = '';
        this.medKit.suggestionsOpen = false;
    }

    clearAllWarnings() {

        const medKitPills = this.medKit.pills;

        for (let pill of medKitPills) {

            pill.button.classList.remove('warning');
        }
    }

    dataSafeName(string) {

        const regex = new RegExp(this.medKit.pillDataDelimiter, 'gi');
        const safeString = string.replace(regex, this.medKit.unsafeKeyCodesReplacement)

        return safeString.toLowerCase().trim();
    }
}
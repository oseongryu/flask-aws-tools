class CompCheckList extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <style>
                .check-list-container {
                    display: flex;
                    flex-direction: column;
                }
                .check-list {
                    display: flex;
                    flex-wrap: wrap;
                    max-width: 300px;
                }
                .check-list label {
                    width: 50px;
                    margin: 5px;
                }
                .result {
                    margin-top: 20px;
                }
            </style>
            <form id="checkForm" >
                <div class="check-list-container">
                    <label><input type="checkbox" id="selectAllCheckbox"> Select All</label>
                    <div class="check-list"></div>
                </div>
            </form>
        `;
    }

    connectedCallback() {
        const checkList = this.shadowRoot.querySelector('.check-list');
        for (let hour = 1; hour < 24; hour++) {
            const label = document.createElement('label');
            label.innerHTML = `<input type="checkbox" name="hours" value="${hour}"> ${hour}`;
            checkList.appendChild(label);
        }

        const selectAllCheckbox = this.shadowRoot.querySelector('#selectAllCheckbox');
        selectAllCheckbox.addEventListener('click', () => {
            const isChecked = selectAllCheckbox.checked;
            const checkboxes = this.shadowRoot.querySelectorAll('input[name="hours"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = isChecked;
            });
        });
    }

    getFormData() {
        const form = this.shadowRoot.querySelector('#checkForm');
        const formClone = $(form).clone();
        formClone.appendTo(document.body);
        const serializedData = formClone.serialize();
        formClone.remove();
        return serializedData;
    }
}

customElements.define('comp-check-list', CompCheckList);
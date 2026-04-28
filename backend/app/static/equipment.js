const equipmentElements = {
    projectSelect: document.getElementById("projectSelect"),
    idInput: document.getElementById("equipmentIdInput"),
    roomNumberInput: document.getElementById("equipmentRoomNumberInput"),
    nameInput: document.getElementById("equipmentNameInput"),
    typeInput: document.getElementById("equipmentTypeInput"),
    individualAddressInput: document.getElementById("equipmentIndividualAddressInput"),
    descriptionInput: document.getElementById("equipmentDescriptionInput"),
    saveButton: document.getElementById("saveEquipmentButton"),
    clearButton: document.getElementById("clearEquipmentFormButton"),
    tableBody: document.getElementById("equipmentTableBody"),
    addressOptions: document.getElementById("equipmentAddressOptions"),
};

let equipmentItems = [];

function equipmentLog(message) {
    if (typeof log === "function") {
        log(message);
    } else {
        console.log(message);
    }
}

function getActiveProjectIdForEquipment() {
    const value = equipmentElements.projectSelect?.value;
    return value ? Number(value) : null;
}

async function equipmentRequestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return await response.json();
}

function clearEquipmentForm() {
    equipmentElements.idInput.value = "";
    equipmentElements.roomNumberInput.value = "";
    equipmentElements.nameInput.value = "";
    equipmentElements.typeInput.value = "";
    equipmentElements.individualAddressInput.value = "";
    equipmentElements.descriptionInput.value = "";

    equipmentElements.saveButton.textContent = "Добавить оборудование";
}

function buildEquipmentPayload() {
    return {
        room_number: equipmentElements.roomNumberInput.value.trim() || null,
        name: equipmentElements.nameInput.value.trim(),
        equipment_type: equipmentElements.typeInput.value.trim() || null,
        individual_address: equipmentElements.individualAddressInput.value.trim(),
        description: equipmentElements.descriptionInput.value.trim() || null,
    };
}

function renderEquipment() {
    if (!equipmentElements.tableBody) {
        return;
    }

    equipmentElements.tableBody.innerHTML = "";

    for (const item of equipmentItems) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.room_number || ""}</td>
            <td>${item.name || ""}</td>
            <td>${item.equipment_type || ""}</td>
            <td>${item.individual_address || ""}</td>
            <td>${item.description || ""}</td>
            <td>
                <button class="secondary" data-edit-equipment-id="${item.id}">Редактировать</button>
                <button class="danger" data-delete-equipment-id="${item.id}">Удалить</button>
            </td>
        `;

        equipmentElements.tableBody.appendChild(tr);
    }

    document.querySelectorAll("[data-edit-equipment-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const item = equipmentItems.find(
                (equipment) => equipment.id === Number(button.dataset.editEquipmentId)
            );

            if (!item) {
                return;
            }

            equipmentElements.idInput.value = item.id;
            equipmentElements.roomNumberInput.value = item.room_number || "";
            equipmentElements.nameInput.value = item.name || "";
            equipmentElements.typeInput.value = item.equipment_type || "";
            equipmentElements.individualAddressInput.value = item.individual_address || "";
            equipmentElements.descriptionInput.value = item.description || "";

            equipmentElements.saveButton.textContent = "Сохранить оборудование";
        });
    });

    document.querySelectorAll("[data-delete-equipment-id]").forEach((button) => {
        button.addEventListener("click", async () => {
            const equipmentId = Number(button.dataset.deleteEquipmentId);
            const confirmed = confirm(`Удалить оборудование ID ${equipmentId}?`);

            if (!confirmed) {
                return;
            }

            await equipmentRequestJson(`/equipment/${equipmentId}`, {
                method: "DELETE",
            });

            equipmentLog(`Оборудование удалено: ID ${equipmentId}`);

            await loadEquipment();
        });
    });
}

function updateEquipmentAddressDatalist() {
    if (!equipmentElements.addressOptions) {
        return;
    }

    equipmentElements.addressOptions.innerHTML = "";

    for (const item of equipmentItems) {
        if (!item.individual_address) {
            continue;
        }

        const option = document.createElement("option");
        option.value = item.individual_address;

        const parts = [
            item.individual_address,
            item.name,
            item.equipment_type,
            item.room_number ? `Помещение ${item.room_number}` : "",
        ].filter(Boolean);

        option.label = parts.join(" — ");
        option.textContent = parts.join(" — ");

        equipmentElements.addressOptions.appendChild(option);
    }

    refreshEquipmentAddressSelectOptions();
}


function buildEquipmentOptionText(item) {
    const parts = [
        item.individual_address,
        item.name,
        item.equipment_type,
        item.room_number ? `Помещение ${item.room_number}` : "",
    ].filter(Boolean);

    return parts.join(" — ");
}

function createEquipmentAddressSelectForInput(input) {
    if (!input || input.dataset.equipmentSelectAttached === "true") {
        return;
    }

    const select = document.createElement("select");
    select.className = "equipment-address-select";
    select.dataset.targetInputId = input.id;

    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.textContent = "Выбрать из справочника оборудования";
    select.appendChild(emptyOption);

    select.addEventListener("change", () => {
        if (!select.value) {
            return;
        }

        input.value = select.value;

        const equipment = equipmentItems.find(
            (item) => item.individual_address === select.value
        );

        if (equipment) {
            const equipmentType = equipment.equipment_type || "";

            const targetTypeMap = {
                lightingDeviceAddressInput: "lightingDeviceTypeInput",
                mechanismDeviceAddressInput: "mechanismDeviceTypeInput",
                fanDeviceAddressInput: "fanDeviceTypeInput",
                floorHeatingDeviceAddressInput: "floorHeatingDeviceTypeInput",
                climateDeviceAddressInput: "climateDeviceTypeInput",
            };

            const typeInputId = targetTypeMap[input.id];
            const typeInput = typeInputId ? document.getElementById(typeInputId) : null;

            if (typeInput && equipmentType && !typeInput.value.trim()) {
                typeInput.value = equipmentType;
            }
        }
    });

    input.insertAdjacentElement("afterend", select);
    input.dataset.equipmentSelectAttached = "true";
}

function refreshEquipmentAddressSelectOptions() {
    document.querySelectorAll(".equipment-address-select").forEach((select) => {
        const currentValue = select.value;

        select.innerHTML = "";

        const emptyOption = document.createElement("option");
        emptyOption.value = "";
        emptyOption.textContent = "Выбрать из справочника оборудования";
        select.appendChild(emptyOption);

        for (const item of equipmentItems) {
            if (!item.individual_address) {
                continue;
            }

            const option = document.createElement("option");
            option.value = item.individual_address;
            option.textContent = buildEquipmentOptionText(item);
            select.appendChild(option);
        }

        select.value = currentValue;
    });
}

function attachEquipmentAddressSuggestions() {
    const inputIds = [
        "lightingDeviceAddressInput",
        "socketContactorDeviceAddressInput",
        "mechanismDeviceAddressInput",
        "fanDeviceAddressInput",
        "floorHeatingDeviceAddressInput",
        "climateDeviceAddressInput",
        "climateGatewayAddressInput",
    ];

    for (const inputId of inputIds) {
        const input = document.getElementById(inputId);

        if (input) {
            input.setAttribute("list", "equipmentAddressOptions");
            createEquipmentAddressSelectForInput(input);
        }
    }

    refreshEquipmentAddressSelectOptions();
}

async function loadEquipment() {
    const projectId = getActiveProjectIdForEquipment();

    if (!projectId) {
        equipmentItems = [];
        renderEquipment();
        updateEquipmentAddressDatalist();
        return;
    }

    equipmentItems = await equipmentRequestJson(`/projects/${projectId}/equipment`);

    renderEquipment();
    updateEquipmentAddressDatalist();
    attachEquipmentAddressSuggestions();
}

async function saveEquipment() {
    const projectId = getActiveProjectIdForEquipment();

    if (!projectId) {
        equipmentLog("Сначала выберите проект");
        return;
    }

    const payload = buildEquipmentPayload();

    if (!payload.name || !payload.individual_address) {
        equipmentLog("Заполните название оборудования и индивидуальный адрес");
        return;
    }

    const equipmentId = equipmentElements.idInput.value.trim();

    if (equipmentId) {
        await equipmentRequestJson(`/equipment/${equipmentId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
            },
            body: JSON.stringify(payload),
        });

        equipmentLog(`Оборудование обновлено: ${payload.individual_address} ${payload.name}`);
    } else {
        await equipmentRequestJson(`/projects/${projectId}/equipment`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
            },
            body: JSON.stringify(payload),
        });

        equipmentLog(`Оборудование добавлено: ${payload.individual_address} ${payload.name}`);
    }

    clearEquipmentForm();
    await loadEquipment();
}

function bindEquipmentEvents() {
    if (equipmentElements.saveButton) {
        equipmentElements.saveButton.addEventListener("click", () => {
            saveEquipment().catch((error) => equipmentLog(error.message));
        });
    }

    if (equipmentElements.clearButton) {
        equipmentElements.clearButton.addEventListener("click", clearEquipmentForm);
    }

    if (equipmentElements.projectSelect) {
        equipmentElements.projectSelect.addEventListener("change", () => {
            clearEquipmentForm();
            loadEquipment().catch((error) => equipmentLog(error.message));
        });
    }

    document.querySelectorAll('.tab-button[data-tab="equipment"]').forEach((button) => {
        button.addEventListener("click", () => {
            loadEquipment().catch((error) => equipmentLog(error.message));
        });
    });
}

bindEquipmentEvents();
attachEquipmentAddressSuggestions();
setTimeout(() => {
    loadEquipment().catch((error) => equipmentLog(error.message));
}, 800);



/* Equipment catalog selects for device type and individual address.
   Original inputs stay in DOM so existing save/update code keeps working.
   Device type dropdown is used only for lighting.
*/
(function initEquipmentCatalogProxySelects() {
    const LIGHTING_DEVICE_TYPE_OPTIONS = [
        "DALI",
        "RELAY",
    ];

    const addressInputIds = [
        "lightingDeviceAddressInput",
        "mechanismDeviceAddressInput",
        "fanDeviceAddressInput",
        "floorHeatingDeviceAddressInput",
        "climateDeviceAddressInput",
        "climateGatewayAddressInput",
        "socketContactorDeviceAddressInput",
    ];

    const typeInputIds = [
        "lightingDeviceTypeInput",
    ];

    const addressToTypeInputMap = {
        lightingDeviceAddressInput: "lightingDeviceTypeInput",
        socketContactorDeviceAddressInput: "socketContactorDeviceTypeInput",
    };

    function getCatalogItems() {
        try {
            return Array.isArray(equipmentItems) ? equipmentItems : [];
        } catch {
            return [];
        }
    }

    function buildCatalogText(item) {
        const parts = [
            item.individual_address,
            item.name,
            item.equipment_type,
            item.room_number ? `Помещение ${item.room_number}` : "",
        ].filter(Boolean);

        return parts.join(" — ");
    }

    function removeOldProxySelects() {
        document.querySelectorAll(".equipment-address-select").forEach((select) => {
            select.remove();
        });

        document.querySelectorAll(".equipment-catalog-select").forEach((select) => {
            const targetInputId = select.dataset.targetInputId;
            const input = targetInputId ? document.getElementById(targetInputId) : null;

            if (input) {
                input.classList.remove("equipment-original-input-hidden");
                delete input.dataset.catalogProxyAttached;
            }

            select.remove();
        });
    }

    function ensureProxySelect(input, mode) {
        if (!input || input.dataset.catalogProxyAttached === "true") {
            return;
        }

        const select = document.createElement("select");
        select.className = "equipment-catalog-select";
        select.dataset.targetInputId = input.id;
        select.dataset.mode = mode;

        select.addEventListener("change", () => {
            if (select.value === "__manual__") {
                input.classList.remove("equipment-original-input-hidden");
                input.focus();
                select.value = "";
                return;
            }

            input.classList.add("equipment-original-input-hidden");
            input.value = select.value;

            if (mode === "address") {
                const item = getCatalogItems().find(
                    (equipment) => equipment.individual_address === select.value
                );

                if (item && item.equipment_type) {
                    const typeInputId = addressToTypeInputMap[input.id];
                    const typeInput = typeInputId ? document.getElementById(typeInputId) : null;

                    if (typeInput) {
                        const normalizedType = String(item.equipment_type).trim().toUpperCase();

                        if (normalizedType === "DALI" || normalizedType === "RELAY") {
                            typeInput.value = normalizedType;
                            refreshCatalogProxySelect(typeInput);
                        }
                    }
                }
            }
        });

        input.insertAdjacentElement("afterend", select);
        input.classList.add("equipment-original-input-hidden");
        input.dataset.catalogProxyAttached = "true";

        refreshCatalogProxySelect(input);
    }

    function fillBaseOptions(select, placeholder) {
        select.innerHTML = "";

        const emptyOption = document.createElement("option");
        emptyOption.value = "";
        emptyOption.textContent = placeholder;
        select.appendChild(emptyOption);
    }

    function addManualOption(select) {
        const manualOption = document.createElement("option");
        manualOption.value = "__manual__";
        manualOption.textContent = "Ручной ввод";
        select.appendChild(manualOption);
    }

    function refreshCatalogProxySelect(input) {
        if (!input) {
            return;
        }

        const select = document.querySelector(
            `.equipment-catalog-select[data-target-input-id="${input.id}"]`
        );

        if (!select) {
            return;
        }

        const mode = select.dataset.mode;
        const currentValue = input.value.trim();

        if (mode === "address") {
            fillBaseOptions(select, "Выберите адрес устройства");

            const used = new Set();

            for (const item of getCatalogItems()) {
                if (!item.individual_address || used.has(item.individual_address)) {
                    continue;
                }

                used.add(item.individual_address);

                const option = document.createElement("option");
                option.value = item.individual_address;
                option.textContent = buildCatalogText(item);
                select.appendChild(option);
            }

            if (currentValue && !used.has(currentValue)) {
                const currentOption = document.createElement("option");
                currentOption.value = currentValue;
                currentOption.textContent = `Текущее значение: ${currentValue}`;
                select.appendChild(currentOption);
            }

            addManualOption(select);
            select.value = currentValue;
            return;
        }

        if (mode === "type") {
            fillBaseOptions(select, "Выберите тип устройства");

            const types = new Set(LIGHTING_DEVICE_TYPE_OPTIONS);

            const normalizedCurrentValue = currentValue.toUpperCase();
            if (normalizedCurrentValue === "DALI" || normalizedCurrentValue === "RELAY") {
                types.add(normalizedCurrentValue);
            }

            for (const type of Array.from(types).sort()) {
                const option = document.createElement("option");
                option.value = type;
                option.textContent = type;
                select.appendChild(option);
            }

            addManualOption(select);

            if (normalizedCurrentValue === "DALI" || normalizedCurrentValue === "RELAY") {
                select.value = normalizedCurrentValue;
                input.value = normalizedCurrentValue;
            } else {
                select.value = "";
            }
        }
    }

    function refreshAllCatalogProxySelects() {
        for (const inputId of [...addressInputIds, ...typeInputIds]) {
            refreshCatalogProxySelect(document.getElementById(inputId));
        }
    }

    function attachCatalogProxySelects() {
        removeOldProxySelects();

        for (const inputId of addressInputIds) {
            ensureProxySelect(document.getElementById(inputId), "address");
        }

        for (const inputId of typeInputIds) {
            ensureProxySelect(document.getElementById(inputId), "type");
        }

        refreshAllCatalogProxySelects();
    }

    if (typeof loadEquipment === "function" && loadEquipment.__catalogProxyPatched !== true) {
        const originalLoadEquipment = loadEquipment;

        loadEquipment = async function patchedLoadEquipment(...args) {
            const result = await originalLoadEquipment.apply(this, args);
            attachCatalogProxySelects();
            refreshAllCatalogProxySelects();
            return result;
        };

        loadEquipment.__catalogProxyPatched = true;
    }

    window.attachCatalogProxySelects = attachCatalogProxySelects;
    window.refreshAllCatalogProxySelects = refreshAllCatalogProxySelects;

    setTimeout(attachCatalogProxySelects, 500);
    setTimeout(refreshAllCatalogProxySelects, 1000);
})();



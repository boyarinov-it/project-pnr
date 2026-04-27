const floorHeatingState = {
    items: [],
};

const floorHeatingElements = {
    idInput: document.getElementById("floorHeatingIdInput"),
    roomNumberInput: document.getElementById("floorHeatingRoomNumberInput"),
    nameInput: document.getElementById("floorHeatingNameInput"),
    codeInput: document.getElementById("floorHeatingCodeInput"),
    thermostatTypeInput: document.getElementById("floorHeatingThermostatTypeInput"),
    quantityInput: document.getElementById("floorHeatingQuantityInput"),
    deviceTypeInput: document.getElementById("floorHeatingDeviceTypeInput"),
    deviceAddressInput: document.getElementById("floorHeatingDeviceAddressInput"),
    deviceChannelInput: document.getElementById("floorHeatingDeviceChannelInput"),
    saveButton: document.getElementById("saveFloorHeatingButton"),
    clearButton: document.getElementById("clearFloorHeatingFormButton"),
    tableBody: document.getElementById("floorHeatingTableBody"),
    projectSelect: document.getElementById("projectSelect"),
    logOutput: document.getElementById("logOutput"),
};

function floorHeatingLog(message) {
    const time = new Date().toLocaleTimeString();
    floorHeatingElements.logOutput.textContent = `[${time}] ${message}\n` + floorHeatingElements.logOutput.textContent;
}

function floorHeatingEscapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function getActiveProjectIdForFloorHeating() {
    const value = floorHeatingElements.projectSelect.value;
    return value ? Number(value) : null;
}

async function floorHeatingRequestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return response.json();
}

async function loadFloorHeating() {
    const projectId = getActiveProjectIdForFloorHeating();

    if (!projectId) {
        floorHeatingElements.tableBody.innerHTML = "";
        return;
    }

    floorHeatingState.items = await floorHeatingRequestJson(`/projects/${projectId}/floor-heating`);
    renderFloorHeating();
}

function renderFloorHeating() {
    floorHeatingElements.tableBody.innerHTML = "";

    for (const item of floorHeatingState.items) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${floorHeatingEscapeHtml(item.id)}</td>
            <td>${floorHeatingEscapeHtml(item.room_number)} ${floorHeatingEscapeHtml(item.room_name)}</td>
            <td>${floorHeatingEscapeHtml(item.name)}</td>
            <td>${floorHeatingEscapeHtml(item.code)}</td>
            <td>${floorHeatingEscapeHtml(item.thermostat_type)}</td>
            <td>${floorHeatingEscapeHtml(item.quantity)}</td>
            <td>${floorHeatingEscapeHtml(item.device_type)}</td>
            <td>${floorHeatingEscapeHtml(item.device_address)}</td>
            <td>${floorHeatingEscapeHtml(item.device_channel)}</td>
            <td>
                <div class="table-actions">
                    <button type="button" data-floor-heating-edit-id="${floorHeatingEscapeHtml(item.id)}" class="secondary">Редактировать</button>
                    <button type="button" data-floor-heating-delete-id="${floorHeatingEscapeHtml(item.id)}" class="danger">Удалить</button>
                </div>
            </td>
        `;

        floorHeatingElements.tableBody.appendChild(tr);
    }

    floorHeatingElements.tableBody.querySelectorAll("button[data-floor-heating-edit-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const itemId = Number(button.dataset.floorHeatingEditId);
            const item = floorHeatingState.items.find((x) => x.id === itemId);

            if (item) {
                fillFloorHeatingForm(item);
            }
        });
    });

    floorHeatingElements.tableBody.querySelectorAll("button[data-floor-heating-delete-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const itemId = Number(button.dataset.floorHeatingDeleteId);
            deleteFloorHeating(itemId).catch((error) => floorHeatingLog(error.message));
        });
    });
}

function fillFloorHeatingForm(item) {
    floorHeatingElements.idInput.value = item.id;
    floorHeatingElements.roomNumberInput.value = item.room_number ?? "";
    floorHeatingElements.nameInput.value = item.name ?? "";
    floorHeatingElements.codeInput.value = item.code ?? "";
    floorHeatingElements.thermostatTypeInput.value = item.thermostat_type ?? "";
    floorHeatingElements.quantityInput.value = item.quantity ?? 1;
    floorHeatingElements.deviceTypeInput.value = item.device_type ?? "";
    floorHeatingElements.deviceAddressInput.value = item.device_address ?? "";
    floorHeatingElements.deviceChannelInput.value = item.device_channel ?? "";
    floorHeatingElements.saveButton.textContent = "Сохранить теплый пол";
}

function clearFloorHeatingForm() {
    floorHeatingElements.idInput.value = "";
    floorHeatingElements.roomNumberInput.value = "";
    floorHeatingElements.nameInput.value = "";
    floorHeatingElements.codeInput.value = "";
    floorHeatingElements.thermostatTypeInput.value = "";
    floorHeatingElements.quantityInput.value = "1";
    floorHeatingElements.deviceTypeInput.value = "";
    floorHeatingElements.deviceAddressInput.value = "";
    floorHeatingElements.deviceChannelInput.value = "";
    floorHeatingElements.saveButton.textContent = "Добавить теплый пол";
}

function buildFloorHeatingPayload() {
    return {
        room_number: floorHeatingElements.roomNumberInput.value.trim(),
        name: floorHeatingElements.nameInput.value.trim(),
        code: floorHeatingElements.codeInput.value.trim(),
        thermostat_type: floorHeatingElements.thermostatTypeInput.value.trim(),
        quantity: Number(floorHeatingElements.quantityInput.value || 1),
        device_type: floorHeatingElements.deviceTypeInput.value.trim() || null,
        device_address: floorHeatingElements.deviceAddressInput.value.trim() || null,
        device_channel: floorHeatingElements.deviceChannelInput.value.trim() || null,
    };
}

async function saveFloorHeating() {
    const projectId = getActiveProjectIdForFloorHeating();

    if (!projectId) {
        floorHeatingLog("Сначала выберите проект");
        return;
    }

    const itemId = floorHeatingElements.idInput.value.trim();
    const payload = buildFloorHeatingPayload();

    if (!payload.room_number || !payload.name || !payload.code || !payload.thermostat_type) {
        floorHeatingLog("Заполните № помещения, название, код и тип термостата");
        return;
    }

    if (payload.quantity <= 0) {
        floorHeatingLog("Количество должно быть больше 0");
        return;
    }

    if (itemId) {
        await floorHeatingRequestJson(`/floor-heating/${itemId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        floorHeatingLog(`Теплый пол обновлен: ${payload.room_number} ${payload.name}`);
    } else {
        await floorHeatingRequestJson(`/projects/${projectId}/floor-heating`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        floorHeatingLog(`Теплый пол добавлен: ${payload.room_number} ${payload.name}`);
    }

    clearFloorHeatingForm();
    await loadFloorHeating();
}

async function deleteFloorHeating(itemId) {
    const confirmed = confirm(`Удалить теплый пол ID ${itemId}?`);

    if (!confirmed) {
        return;
    }

    await floorHeatingRequestJson(`/floor-heating/${itemId}`, {
        method: "DELETE",
    });

    floorHeatingLog(`Теплый пол удален: ID ${itemId}`);
    await loadFloorHeating();
}

document.querySelectorAll('.tab-button[data-tab="floor-heating"]').forEach((button) => {
    button.addEventListener("click", () => {
        loadFloorHeating().catch((error) => floorHeatingLog(error.message));
    });
});

floorHeatingElements.projectSelect.addEventListener("change", () => {
    clearFloorHeatingForm();

    const panel = document.getElementById("tab-floor-heating");
    if (panel && panel.classList.contains("active")) {
        loadFloorHeating().catch((error) => floorHeatingLog(error.message));
    }
});

floorHeatingElements.saveButton.addEventListener("click", () => {
    saveFloorHeating().catch((error) => floorHeatingLog(error.message));
});

floorHeatingElements.clearButton.addEventListener("click", clearFloorHeatingForm);

const climateState = {
    items: [],
};

const climateElements = {
    idInput: document.getElementById("climateIdInput"),
    roomNumberInput: document.getElementById("climateRoomNumberInput"),
    nameInput: document.getElementById("climateNameInput"),
    codeInput: document.getElementById("climateCodeInput"),
    climateTypeInput: document.getElementById("climateTypeInput"),
    quantityInput: document.getElementById("climateQuantityInput"),
    deviceTypeInput: document.getElementById("climateDeviceTypeInput"),
    deviceAddressInput: document.getElementById("climateDeviceAddressInput"),
    deviceChannelInput: document.getElementById("climateDeviceChannelInput"),
    gatewayAddressInput: document.getElementById("climateGatewayAddressInput"),
    externalIdInput: document.getElementById("climateExternalIdInput"),
    saveButton: document.getElementById("saveClimateButton"),
    clearButton: document.getElementById("clearClimateFormButton"),
    tableBody: document.getElementById("climateTableBody"),
    projectSelect: document.getElementById("projectSelect"),
    logOutput: document.getElementById("logOutput"),
};

function climateLog(message) {
    const time = new Date().toLocaleTimeString();
    climateElements.logOutput.textContent = `[${time}] ${message}\n` + climateElements.logOutput.textContent;
}

function climateEscapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function getActiveProjectIdForClimate() {
    const value = climateElements.projectSelect.value;
    return value ? Number(value) : null;
}

async function climateRequestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return response.json();
}

async function loadClimate() {
    const projectId = getActiveProjectIdForClimate();

    if (!projectId) {
        climateElements.tableBody.innerHTML = "";
        return;
    }

    climateState.items = await climateRequestJson(`/projects/${projectId}/climate`);
    renderClimate();
}

function renderClimate() {
    climateElements.tableBody.innerHTML = "";

    for (const item of climateState.items) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${climateEscapeHtml(item.id)}</td>
            <td>${climateEscapeHtml(item.room_number)} ${climateEscapeHtml(item.room_name)}</td>
            <td>${climateEscapeHtml(item.name)}</td>
            <td>${climateEscapeHtml(item.code)}</td>
            <td>${climateEscapeHtml(item.climate_type)}</td>
            <td>${climateEscapeHtml(item.quantity)}</td>
            <td>${climateEscapeHtml(item.device_type)}</td>
            <td>${climateEscapeHtml(item.device_address)}</td>
            <td>${climateEscapeHtml(item.device_channel)}</td>
            <td>${climateEscapeHtml(item.gateway_address)}</td>
            <td>${climateEscapeHtml(item.external_id)}</td>
            <td>
                <div class="table-actions">
                    <button type="button" data-climate-edit-id="${climateEscapeHtml(item.id)}" class="secondary">Редактировать</button>
                    <button type="button" data-climate-delete-id="${climateEscapeHtml(item.id)}" class="danger">Удалить</button>
                </div>
            </td>
        `;

        climateElements.tableBody.appendChild(tr);
    }

    climateElements.tableBody.querySelectorAll("button[data-climate-edit-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const itemId = Number(button.dataset.climateEditId);
            const item = climateState.items.find((x) => x.id === itemId);

            if (item) {
                fillClimateForm(item);
            }
        });
    });

    climateElements.tableBody.querySelectorAll("button[data-climate-delete-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const itemId = Number(button.dataset.climateDeleteId);
            deleteClimate(itemId).catch((error) => climateLog(error.message));
        });
    });
}

function fillClimateForm(item) {
    climateElements.idInput.value = item.id;
    climateElements.roomNumberInput.value = item.room_number ?? "";
    climateElements.nameInput.value = item.name ?? "";
    climateElements.codeInput.value = item.code ?? "";
    climateElements.climateTypeInput.value = item.climate_type ?? "AC";
    climateElements.quantityInput.value = item.quantity ?? 1;
    climateElements.deviceTypeInput.value = item.device_type ?? "";
    climateElements.deviceAddressInput.value = item.device_address ?? "";
    climateElements.deviceChannelInput.value = item.device_channel ?? "";
    climateElements.gatewayAddressInput.value = item.gateway_address ?? "";
    climateElements.externalIdInput.value = item.external_id ?? "";
    climateElements.saveButton.textContent = "Сохранить климат";
}

function clearClimateForm() {
    climateElements.idInput.value = "";
    climateElements.roomNumberInput.value = "";
    climateElements.nameInput.value = "";
    climateElements.codeInput.value = "";
    climateElements.climateTypeInput.value = "AC";
    climateElements.quantityInput.value = "1";
    climateElements.deviceTypeInput.value = "";
    climateElements.deviceAddressInput.value = "";
    climateElements.deviceChannelInput.value = "";
    climateElements.gatewayAddressInput.value = "";
    climateElements.externalIdInput.value = "";
    climateElements.saveButton.textContent = "Добавить климат";
}

function buildClimatePayload() {
    return {
        room_number: climateElements.roomNumberInput.value.trim(),
        name: climateElements.nameInput.value.trim(),
        code: climateElements.codeInput.value.trim(),
        climate_type: climateElements.climateTypeInput.value,
        quantity: Number(climateElements.quantityInput.value || 1),
        device_type: climateElements.deviceTypeInput.value.trim() || null,
        device_address: climateElements.deviceAddressInput.value.trim() || null,
        device_channel: climateElements.deviceChannelInput.value.trim() || null,
        gateway_address: climateElements.gatewayAddressInput.value.trim() || null,
        external_id: climateElements.externalIdInput.value.trim() || null,
    };
}

async function saveClimate() {
    const projectId = getActiveProjectIdForClimate();

    if (!projectId) {
        climateLog("Сначала выберите проект");
        return;
    }

    const itemId = climateElements.idInput.value.trim();
    const payload = buildClimatePayload();

    if (!payload.room_number || !payload.name || !payload.code || !payload.climate_type) {
        climateLog("Заполните № помещения, название, код и тип климата");
        return;
    }

    if (payload.quantity <= 0) {
        climateLog("Количество должно быть больше 0");
        return;
    }

    if (itemId) {
        await climateRequestJson(`/climate/${itemId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        climateLog(`Климат обновлен: ${payload.room_number} ${payload.name}`);
    } else {
        await climateRequestJson(`/projects/${projectId}/climate`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        climateLog(`Климат добавлен: ${payload.room_number} ${payload.name}`);
    }

    clearClimateForm();
    await loadClimate();
}

async function deleteClimate(itemId) {
    const confirmed = confirm(`Удалить климат ID ${itemId}?`);

    if (!confirmed) {
        return;
    }

    await climateRequestJson(`/climate/${itemId}`, {
        method: "DELETE",
    });

    climateLog(`Климат удален: ID ${itemId}`);
    await loadClimate();
}

document.querySelectorAll('.tab-button[data-tab="climate"]').forEach((button) => {
    button.addEventListener("click", () => {
        loadClimate().catch((error) => climateLog(error.message));
    });
});

climateElements.projectSelect.addEventListener("change", () => {
    clearClimateForm();

    const panel = document.getElementById("tab-climate");
    if (panel && panel.classList.contains("active")) {
        loadClimate().catch((error) => climateLog(error.message));
    }
});

climateElements.saveButton.addEventListener("click", () => {
    saveClimate().catch((error) => climateLog(error.message));
});

climateElements.clearButton.addEventListener("click", clearClimateForm);

const mechanismsState = {
    items: [],
};

const mechanismElements = {
    idInput: document.getElementById("mechanismIdInput"),
    roomNumberInput: document.getElementById("mechanismRoomNumberInput"),
    nameInput: document.getElementById("mechanismNameInput"),
    codeInput: document.getElementById("mechanismCodeInput"),
    typeInput: document.getElementById("mechanismTypeInput"),
    quantityInput: document.getElementById("mechanismQuantityInput"),
    deviceTypeInput: document.getElementById("mechanismDeviceTypeInput"),
    deviceAddressInput: document.getElementById("mechanismDeviceAddressInput"),
    deviceChannelInput: document.getElementById("mechanismDeviceChannelInput"),
    saveButton: document.getElementById("saveMechanismButton"),
    clearButton: document.getElementById("clearMechanismFormButton"),
    tableBody: document.getElementById("mechanismsTableBody"),
    projectSelect: document.getElementById("projectSelect"),
    logOutput: document.getElementById("logOutput"),
};

function mechanismLog(message) {
    const time = new Date().toLocaleTimeString();
    mechanismElements.logOutput.textContent = `[${time}] ${message}\n` + mechanismElements.logOutput.textContent;
}

function mechanismEscapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function getActiveProjectIdForMechanisms() {
    const value = mechanismElements.projectSelect.value;
    return value ? Number(value) : null;
}

async function mechanismRequestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return response.json();
}

async function loadMechanisms() {
    const projectId = getActiveProjectIdForMechanisms();

    if (!projectId) {
        mechanismElements.tableBody.innerHTML = "";
        return;
    }

    mechanismsState.items = await mechanismRequestJson(`/projects/${projectId}/mechanisms`);
    renderMechanisms();
}

function renderMechanisms() {
    mechanismElements.tableBody.innerHTML = "";

    for (const mechanism of mechanismsState.items) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${mechanismEscapeHtml(mechanism.id)}</td>
            <td>${mechanismEscapeHtml(mechanism.room_number)} ${mechanismEscapeHtml(mechanism.room_name)}</td>
            <td>${mechanismEscapeHtml(mechanism.name)}</td>
            <td>${mechanismEscapeHtml(mechanism.code)}</td>
            <td>${mechanismEscapeHtml(mechanism.mechanism_type)}</td>
            <td>${mechanismEscapeHtml(mechanism.quantity)}</td>
            <td>${mechanismEscapeHtml(mechanism.device_type)}</td>
            <td>${mechanismEscapeHtml(mechanism.device_address)}</td>
            <td>${mechanismEscapeHtml(mechanism.device_channel)}</td>
            <td>
                <div class="table-actions">
                    <button type="button" data-mechanism-edit-id="${mechanismEscapeHtml(mechanism.id)}" class="secondary">Редактировать</button>
                    <button type="button" data-mechanism-delete-id="${mechanismEscapeHtml(mechanism.id)}" class="danger">Удалить</button>
                </div>
            </td>
        `;

        mechanismElements.tableBody.appendChild(tr);
    }

    mechanismElements.tableBody.querySelectorAll("button[data-mechanism-edit-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const mechanismId = Number(button.dataset.mechanismEditId);
            const mechanism = mechanismsState.items.find((item) => item.id === mechanismId);

            if (mechanism) {
                fillMechanismForm(mechanism);
            }
        });
    });

    mechanismElements.tableBody.querySelectorAll("button[data-mechanism-delete-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const mechanismId = Number(button.dataset.mechanismDeleteId);
            deleteMechanism(mechanismId).catch((error) => mechanismLog(error.message));
        });
    });
}

function fillMechanismForm(mechanism) {
    mechanismElements.idInput.value = mechanism.id;
    mechanismElements.roomNumberInput.value = mechanism.room_number ?? "";
    mechanismElements.nameInput.value = mechanism.name ?? "";
    mechanismElements.codeInput.value = mechanism.code ?? "";
    mechanismElements.typeInput.value = mechanism.mechanism_type ?? "SHUTTER";
    mechanismElements.quantityInput.value = mechanism.quantity ?? 1;
    mechanismElements.deviceTypeInput.value = mechanism.device_type ?? "";
    mechanismElements.deviceAddressInput.value = mechanism.device_address ?? "";
    mechanismElements.deviceChannelInput.value = mechanism.device_channel ?? "";
    mechanismElements.saveButton.textContent = "Сохранить механизм";
}

function clearMechanismForm() {
    mechanismElements.idInput.value = "";
    mechanismElements.roomNumberInput.value = "";
    mechanismElements.nameInput.value = "";
    mechanismElements.codeInput.value = "";
    mechanismElements.typeInput.value = "SHUTTER";
    mechanismElements.quantityInput.value = "1";
    mechanismElements.deviceTypeInput.value = "";
    mechanismElements.deviceAddressInput.value = "";
    mechanismElements.deviceChannelInput.value = "";
    mechanismElements.saveButton.textContent = "Добавить механизм";
}

function buildMechanismPayload() {
    return {
        room_number: mechanismElements.roomNumberInput.value.trim(),
        name: mechanismElements.nameInput.value.trim(),
        code: mechanismElements.codeInput.value.trim(),
        mechanism_type: mechanismElements.typeInput.value,
        quantity: Number(mechanismElements.quantityInput.value || 1),
        device_type: mechanismElements.deviceTypeInput.value.trim() || null,
        device_address: mechanismElements.deviceAddressInput.value.trim() || null,
        device_channel: mechanismElements.deviceChannelInput.value.trim() || null,
    };
}

async function saveMechanism() {
    const projectId = getActiveProjectIdForMechanisms();

    if (!projectId) {
        mechanismLog("Сначала выберите проект");
        return;
    }

    const mechanismId = mechanismElements.idInput.value.trim();
    const payload = buildMechanismPayload();

    if (!payload.room_number || !payload.name || !payload.code || !payload.mechanism_type) {
        mechanismLog("Заполните № помещения, название, код и тип механизма");
        return;
    }

    if (payload.quantity <= 0) {
        mechanismLog("Количество должно быть больше 0");
        return;
    }

    if (mechanismId) {
        await mechanismRequestJson(`/mechanisms/${mechanismId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        mechanismLog(`Механизм обновлен: ${payload.room_number} ${payload.name}`);
    } else {
        await mechanismRequestJson(`/projects/${projectId}/mechanisms`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        mechanismLog(`Механизм добавлен: ${payload.room_number} ${payload.name}`);
    }

    clearMechanismForm();
    await loadMechanisms();
}

async function deleteMechanism(mechanismId) {
    const confirmed = confirm(`Удалить механизм ID ${mechanismId}?`);

    if (!confirmed) {
        return;
    }

    await mechanismRequestJson(`/mechanisms/${mechanismId}`, {
        method: "DELETE",
    });

    mechanismLog(`Механизм удален: ID ${mechanismId}`);
    await loadMechanisms();
}

document.querySelectorAll('.tab-button[data-tab="mechanisms"]').forEach((button) => {
    button.addEventListener("click", () => {
        loadMechanisms().catch((error) => mechanismLog(error.message));
    });
});

mechanismElements.projectSelect.addEventListener("change", () => {
    clearMechanismForm();

    const panel = document.getElementById("tab-mechanisms");
    if (panel && panel.classList.contains("active")) {
        loadMechanisms().catch((error) => mechanismLog(error.message));
    }
});

mechanismElements.saveButton.addEventListener("click", () => {
    saveMechanism().catch((error) => mechanismLog(error.message));
});

mechanismElements.clearButton.addEventListener("click", clearMechanismForm);

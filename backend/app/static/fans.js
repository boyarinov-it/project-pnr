const fansState = {
    items: [],
};

const fanElements = {
    idInput: document.getElementById("fanIdInput"),
    roomNumberInput: document.getElementById("fanRoomNumberInput"),
    nameInput: document.getElementById("fanNameInput"),
    codeInput: document.getElementById("fanCodeInput"),
    quantityInput: document.getElementById("fanQuantityInput"),
    deviceTypeInput: document.getElementById("fanDeviceTypeInput"),
    deviceAddressInput: document.getElementById("fanDeviceAddressInput"),
    deviceChannelInput: document.getElementById("fanDeviceChannelInput"),
    saveButton: document.getElementById("saveFanButton"),
    clearButton: document.getElementById("clearFanFormButton"),
    tableBody: document.getElementById("fansTableBody"),
    projectSelect: document.getElementById("projectSelect"),
    logOutput: document.getElementById("logOutput"),
};

function fanLog(message) {
    const time = new Date().toLocaleTimeString();
    fanElements.logOutput.textContent = `[${time}] ${message}\n` + fanElements.logOutput.textContent;
}

function fanEscapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function getActiveProjectIdForFans() {
    const value = fanElements.projectSelect.value;
    return value ? Number(value) : null;
}

async function fanRequestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return response.json();
}

async function loadFans() {
    const projectId = getActiveProjectIdForFans();

    if (!projectId) {
        fanElements.tableBody.innerHTML = "";
        return;
    }

    fansState.items = await fanRequestJson(`/projects/${projectId}/fans`);
    renderFans();
}

function renderFans() {
    fanElements.tableBody.innerHTML = "";

    for (const fan of fansState.items) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${fanEscapeHtml(fan.id)}</td>
            <td>${fanEscapeHtml(fan.room_number)} ${fanEscapeHtml(fan.room_name)}</td>
            <td>${fanEscapeHtml(fan.name)}</td>
            <td>${fanEscapeHtml(fan.code)}</td>
            <td>${fanEscapeHtml(fan.quantity)}</td>
            <td>${fanEscapeHtml(fan.device_type)}</td>
            <td>${fanEscapeHtml(fan.device_address)}</td>
            <td>${fanEscapeHtml(fan.device_channel)}</td>
            <td>
                <div class="table-actions">
                    <button type="button" data-fan-edit-id="${fanEscapeHtml(fan.id)}" class="secondary">Редактировать</button>
                    <button type="button" data-fan-delete-id="${fanEscapeHtml(fan.id)}" class="danger">Удалить</button>
                </div>
            </td>
        `;

        fanElements.tableBody.appendChild(tr);
    }

    fanElements.tableBody.querySelectorAll("button[data-fan-edit-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const fanId = Number(button.dataset.fanEditId);
            const fan = fansState.items.find((item) => item.id === fanId);

            if (fan) {
                fillFanForm(fan);
            }
        });
    });

    fanElements.tableBody.querySelectorAll("button[data-fan-delete-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const fanId = Number(button.dataset.fanDeleteId);
            deleteFan(fanId).catch((error) => fanLog(error.message));
        });
    });
}

function fillFanForm(fan) {
    fanElements.idInput.value = fan.id;
    fanElements.roomNumberInput.value = fan.room_number ?? "";
    fanElements.nameInput.value = fan.name ?? "";
    fanElements.codeInput.value = fan.code ?? "";
    fanElements.quantityInput.value = fan.quantity ?? 1;
    fanElements.deviceTypeInput.value = fan.device_type ?? "";
    fanElements.deviceAddressInput.value = fan.device_address ?? "";
    fanElements.deviceChannelInput.value = fan.device_channel ?? "";
    fanElements.saveButton.textContent = "Сохранить вентилятор";
}

function clearFanForm() {
    fanElements.idInput.value = "";
    fanElements.roomNumberInput.value = "";
    fanElements.nameInput.value = "";
    fanElements.codeInput.value = "";
    fanElements.quantityInput.value = "1";
    fanElements.deviceTypeInput.value = "";
    fanElements.deviceAddressInput.value = "";
    fanElements.deviceChannelInput.value = "";
    fanElements.saveButton.textContent = "Добавить вентилятор";
}

function buildFanPayload() {
    return {
        room_number: fanElements.roomNumberInput.value.trim(),
        name: fanElements.nameInput.value.trim(),
        code: fanElements.codeInput.value.trim(),
        quantity: Number(fanElements.quantityInput.value || 1),
        device_type: fanElements.deviceTypeInput.value.trim() || null,
        device_address: fanElements.deviceAddressInput.value.trim() || null,
        device_channel: fanElements.deviceChannelInput.value.trim() || null,
    };
}

async function saveFan() {
    const projectId = getActiveProjectIdForFans();

    if (!projectId) {
        fanLog("Сначала выберите проект");
        return;
    }

    const fanId = fanElements.idInput.value.trim();
    const payload = buildFanPayload();

    if (!payload.room_number || !payload.name || !payload.code) {
        fanLog("Заполните № помещения, название и код вентилятора");
        return;
    }

    if (payload.quantity <= 0) {
        fanLog("Количество должно быть больше 0");
        return;
    }

    if (fanId) {
        await fanRequestJson(`/fans/${fanId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        fanLog(`Вентилятор обновлен: ${payload.room_number} ${payload.name}`);
    } else {
        await fanRequestJson(`/projects/${projectId}/fans`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        fanLog(`Вентилятор добавлен: ${payload.room_number} ${payload.name}`);
    }

    clearFanForm();
    await loadFans();
}

async function deleteFan(fanId) {
    const confirmed = confirm(`Удалить вентилятор ID ${fanId}?`);

    if (!confirmed) {
        return;
    }

    await fanRequestJson(`/fans/${fanId}`, {
        method: "DELETE",
    });

    fanLog(`Вентилятор удален: ID ${fanId}`);
    await loadFans();
}

document.querySelectorAll('.tab-button[data-tab="fans"]').forEach((button) => {
    button.addEventListener("click", () => {
        loadFans().catch((error) => fanLog(error.message));
    });
});

fanElements.projectSelect.addEventListener("change", () => {
    clearFanForm();

    const panel = document.getElementById("tab-fans");
    if (panel && panel.classList.contains("active")) {
        loadFans().catch((error) => fanLog(error.message));
    }
});

fanElements.saveButton.addEventListener("click", () => {
    saveFan().catch((error) => fanLog(error.message));
});

fanElements.clearButton.addEventListener("click", clearFanForm);

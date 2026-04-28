const socketsContactorsElements = {
    projectSelect: document.getElementById("projectSelect"),
    idInput: document.getElementById("socketContactorIdInput"),
    roomNumberInput: document.getElementById("socketContactorRoomNumberInput"),
    codeInput: document.getElementById("socketContactorCodeInput"),
    nameInput: document.getElementById("socketContactorNameInput"),
    loadTypeInput: document.getElementById("socketContactorLoadTypeInput"),
    deviceTypeInput: document.getElementById("socketContactorDeviceTypeInput"),
    deviceAddressInput: document.getElementById("socketContactorDeviceAddressInput"),
    deviceOutputInput: document.getElementById("socketContactorDeviceOutputInput"),
    descriptionInput: document.getElementById("socketContactorDescriptionInput"),
    saveButton: document.getElementById("saveSocketContactorButton"),
    clearButton: document.getElementById("clearSocketContactorFormButton"),
    tableBody: document.getElementById("socketsContactorsTableBody"),
};

let socketsContactorsItems = [];
let socketsContactorsRooms = [];

function socketsContactorsLog(message) {
    if (typeof log === "function") {
        log(message);
    } else {
        console.log(message);
    }
}

function getActiveProjectIdForSocketsContactors() {
    const value = socketsContactorsElements.projectSelect?.value;
    return value ? Number(value) : null;
}

async function socketsContactorsRequestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return await response.json();
}

function getSocketContactorSortNumber(item) {
    const code = String(item?.code || "").trim();
    const match = code.match(/\d+/);

    if (!match) {
        return Number.MAX_SAFE_INTEGER;
    }

    return Number(match[0]);
}

function sortSocketsContactors(items) {
    return [...(items || [])].sort((a, b) => {
        const numberA = getSocketContactorSortNumber(a);
        const numberB = getSocketContactorSortNumber(b);

        if (numberA !== numberB) {
            return numberA - numberB;
        }

        return Number(a?.id || 0) - Number(b?.id || 0);
    });
}

function renderSocketContactorRoomOptions() {
    const select = socketsContactorsElements.roomNumberInput;

    if (!select) {
        return;
    }

    const currentValue = select.value;
    select.innerHTML = "";

    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.textContent = "Не выбрано";
    select.appendChild(emptyOption);

    for (const room of socketsContactorsRooms) {
        const option = document.createElement("option");
        option.value = room.room_number;

        const roomName = room.name || room.name_ru || room.code || "";
        option.textContent = roomName
            ? `${room.room_number} — ${roomName}`
            : `${room.room_number}`;

        select.appendChild(option);
    }

    select.value = currentValue;
}

function clearSocketContactorForm() {
    socketsContactorsElements.idInput.value = "";
    socketsContactorsElements.roomNumberInput.value = "";
    socketsContactorsElements.codeInput.value = "";
    socketsContactorsElements.nameInput.value = "";
    socketsContactorsElements.loadTypeInput.value = "SOCKET";
    socketsContactorsElements.deviceTypeInput.value = "";
    socketsContactorsElements.deviceAddressInput.value = "";
    socketsContactorsElements.deviceOutputInput.value = "";
    socketsContactorsElements.descriptionInput.value = "";
    socketsContactorsElements.saveButton.textContent = "Добавить нагрузку";
}

function buildSocketContactorPayload() {
    return {
        room_number: socketsContactorsElements.roomNumberInput.value || null,
        code: socketsContactorsElements.codeInput.value.trim(),
        name: socketsContactorsElements.nameInput.value.trim(),
        load_type: socketsContactorsElements.loadTypeInput.value.trim() || "SOCKET",
        device_type: socketsContactorsElements.deviceTypeInput.value.trim() || null,
        device_address: socketsContactorsElements.deviceAddressInput.value.trim() || null,
        device_output: socketsContactorsElements.deviceOutputInput.value.trim() || null,
        description: socketsContactorsElements.descriptionInput.value.trim() || null,
    };
}

function renderSocketsContactors() {
    const tableBody = socketsContactorsElements.tableBody;

    if (!tableBody) {
        return;
    }

    tableBody.innerHTML = "";

    for (const item of sortSocketsContactors(socketsContactorsItems)) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.room_number || ""}</td>
            <td>${item.code || ""}</td>
            <td>${item.name || ""}</td>
            <td>${item.load_type || ""}</td>
            <td>${item.device_type || ""}</td>
            <td>${item.device_address || ""}</td>
            <td>${item.device_output || ""}</td>
            <td>
                <button class="secondary" data-edit-socket-contactor-id="${item.id}">Редактировать</button>
                <button class="danger" data-delete-socket-contactor-id="${item.id}">Удалить</button>
            </td>
        `;

        tableBody.appendChild(tr);
    }

    document.querySelectorAll("[data-edit-socket-contactor-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const item = socketsContactorsItems.find(
                (candidate) => candidate.id === Number(button.dataset.editSocketContactorId)
            );

            if (!item) {
                return;
            }

            socketsContactorsElements.idInput.value = item.id;
            socketsContactorsElements.roomNumberInput.value = item.room_number || "";
            socketsContactorsElements.codeInput.value = item.code || "";
            socketsContactorsElements.nameInput.value = item.name || "";
            socketsContactorsElements.loadTypeInput.value = item.load_type || "SOCKET";
            socketsContactorsElements.deviceTypeInput.value = item.device_type || "";
            socketsContactorsElements.deviceAddressInput.value = item.device_address || "";
            socketsContactorsElements.deviceOutputInput.value = item.device_output || "";
            socketsContactorsElements.descriptionInput.value = item.description || "";
            socketsContactorsElements.saveButton.textContent = "Сохранить нагрузку";
        });
    });

    document.querySelectorAll("[data-delete-socket-contactor-id]").forEach((button) => {
        button.addEventListener("click", async () => {
            const itemId = Number(button.dataset.deleteSocketContactorId);
            const confirmed = confirm(`Удалить нагрузку ID ${itemId}?`);

            if (!confirmed) {
                return;
            }

            await socketsContactorsRequestJson(`/sockets-contactors/${itemId}`, {
                method: "DELETE",
            });

            socketsContactorsLog(`Розетка/контактор удалены: ID ${itemId}`);
            await loadSocketsContactors();
        });
    });
}

async function loadSocketsContactorsRooms() {
    const projectId = getActiveProjectIdForSocketsContactors();

    if (!projectId) {
        socketsContactorsRooms = [];
        renderSocketContactorRoomOptions();
        return;
    }

    socketsContactorsRooms = await socketsContactorsRequestJson(`/projects/${projectId}/rooms`);
    renderSocketContactorRoomOptions();
}

async function loadSocketsContactors() {
    const projectId = getActiveProjectIdForSocketsContactors();

    if (!projectId) {
        socketsContactorsItems = [];
        renderSocketsContactors();
        return;
    }

    await loadSocketsContactorsRooms();

    socketsContactorsItems = await socketsContactorsRequestJson(
        `/projects/${projectId}/sockets-contactors`
    );

    renderSocketsContactors();

    if (typeof attachCatalogProxySelects === "function") {
        attachCatalogProxySelects();
    }
}

async function saveSocketContactor() {
    const projectId = getActiveProjectIdForSocketsContactors();

    if (!projectId) {
        socketsContactorsLog("Сначала выберите проект");
        return;
    }

    const payload = buildSocketContactorPayload();

    if (!payload.code || !payload.name) {
        socketsContactorsLog("Заполните код и название нагрузки");
        return;
    }

    const itemId = socketsContactorsElements.idInput.value.trim();

    if (itemId) {
        await socketsContactorsRequestJson(`/sockets-contactors/${itemId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
            },
            body: JSON.stringify(payload),
        });

        socketsContactorsLog(`Нагрузка обновлена: ${payload.code} ${payload.name}`);
    } else {
        await socketsContactorsRequestJson(`/projects/${projectId}/sockets-contactors`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
            },
            body: JSON.stringify(payload),
        });

        socketsContactorsLog(`Нагрузка добавлена: ${payload.code} ${payload.name}`);
    }

    clearSocketContactorForm();
    await loadSocketsContactors();
}

function bindSocketsContactorsEvents() {
    if (socketsContactorsElements.saveButton) {
        socketsContactorsElements.saveButton.addEventListener("click", () => {
            saveSocketContactor().catch((error) => socketsContactorsLog(error.message));
        });
    }

    if (socketsContactorsElements.clearButton) {
        socketsContactorsElements.clearButton.addEventListener("click", clearSocketContactorForm);
    }

    if (socketsContactorsElements.projectSelect) {
        socketsContactorsElements.projectSelect.addEventListener("change", () => {
            clearSocketContactorForm();
            loadSocketsContactors().catch((error) => socketsContactorsLog(error.message));
        });
    }

    document.querySelectorAll('.tab-button[data-tab="sockets-contactors"]').forEach((button) => {
        button.addEventListener("click", () => {
            loadSocketsContactors().catch((error) => socketsContactorsLog(error.message));
        });
    });
}

bindSocketsContactorsEvents();

setTimeout(() => {
    loadSocketsContactors().catch((error) => socketsContactorsLog(error.message));
}, 800);

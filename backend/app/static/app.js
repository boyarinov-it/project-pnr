const api = "";

const state = {
    projects: [],
    rooms: [],
    lightingGroups: [],
    activeProjectId: null,
};

const elements = {
    projectNameInput: document.getElementById("projectNameInput"),
    createProjectButton: document.getElementById("createProjectButton"),
    projectSelect: document.getElementById("projectSelect"),
    reloadButton: document.getElementById("reloadButton"),

    roomIdInput: document.getElementById("roomIdInput"),
    roomNumberInput: document.getElementById("roomNumberInput"),
    roomNameRuInput: document.getElementById("roomNameRuInput"),
    roomNameEnInput: document.getElementById("roomNameEnInput"),
    roomCodeInput: document.getElementById("roomCodeInput"),
    saveRoomButton: document.getElementById("saveRoomButton"),
    clearRoomFormButton: document.getElementById("clearRoomFormButton"),
    roomsTableBody: document.getElementById("roomsTableBody"),

    lightingIdInput: document.getElementById("lightingIdInput"),
    lightingRoomNumberInput: document.getElementById("lightingRoomNumberInput"),
    lightingNameInput: document.getElementById("lightingNameInput"),
    lightingCodeInput: document.getElementById("lightingCodeInput"),
    lightingLoadTypeInput: document.getElementById("lightingLoadTypeInput"),
    lightingQuantityInput: document.getElementById("lightingQuantityInput"),
    lightingDeviceTypeInput: document.getElementById("lightingDeviceTypeInput"),
    lightingDeviceAddressInput: document.getElementById("lightingDeviceAddressInput"),
    lightingDeviceOutputInput: document.getElementById("lightingDeviceOutputInput"),
    lightingDimmerChannelInput: document.getElementById("lightingDimmerChannelInput"),
    saveLightingButton: document.getElementById("saveLightingButton"),
    clearLightingFormButton: document.getElementById("clearLightingFormButton"),
    lightingTableBody: document.getElementById("lightingTableBody"),

    logOutput: document.getElementById("logOutput"),
};

function log(message) {
    const time = new Date().toLocaleTimeString();
    elements.logOutput.textContent = `[${time}] ${message}\n` + elements.logOutput.textContent;
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return response.json();
}

function switchTab(tabName) {
    document.querySelectorAll(".tab-button").forEach((button) => {
        button.classList.toggle("active", button.dataset.tab === tabName);
    });

    document.querySelectorAll(".tab-panel").forEach((panel) => {
        panel.classList.toggle("active", panel.id === `tab-${tabName}`);
    });

    if (tabName === "rooms") {
        loadRooms().catch((error) => log(error.message));
    }

    if (tabName === "lighting") {
        loadLightingGroups().catch((error) => log(error.message));
    }
}

async function loadProjects() {
    state.projects = await requestJson(`${api}/projects`);

    elements.projectSelect.innerHTML = "";

    for (const project of state.projects) {
        const option = document.createElement("option");
        option.value = project.id;
        option.textContent = `${project.id} — ${project.name}`;
        elements.projectSelect.appendChild(option);
    }

    if (state.projects.length > 0) {
        state.activeProjectId = Number(elements.projectSelect.value || state.projects[0].id);
        elements.projectSelect.value = String(state.activeProjectId);
        await loadRooms();
        await loadLightingGroups();
    } else {
        state.activeProjectId = null;
        elements.roomsTableBody.innerHTML = "";
        elements.lightingTableBody.innerHTML = "";
    }
}

async function createProject() {
    const name = elements.projectNameInput.value.trim();

    if (!name) {
        log("Введите название проекта");
        return;
    }

    const project = await requestJson(`${api}/projects`, {
        method: "POST",
        headers: {"Content-Type": "application/json; charset=utf-8"},
        body: JSON.stringify({name}),
    });

    elements.projectNameInput.value = "";
    log(`Создан проект: ${project.name}`);
    await loadProjects();

    state.activeProjectId = project.id;
    elements.projectSelect.value = String(project.id);
    await loadRooms();
    await loadLightingGroups();
}

async function loadRooms() {
    if (!state.activeProjectId) {
        return;
    }

    state.rooms = await requestJson(`${api}/projects/${state.activeProjectId}/rooms`);
    renderRooms();
    updateRoomNumberSelects();
    updateRoomNumberDatalist();
}

function renderRooms() {
    elements.roomsTableBody.innerHTML = "";

    for (const room of state.rooms) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${escapeHtml(room.id)}</td>
            <td>${escapeHtml(room.room_number)}</td>
            <td>${escapeHtml(room.name_ru)}</td>
            <td>${escapeHtml(room.name_en)}</td>
            <td>${escapeHtml(room.code)}</td>
            <td>
                <button type="button" data-room-id="${escapeHtml(room.id)}" class="secondary">Редактировать</button>
            </td>
        `;

        elements.roomsTableBody.appendChild(tr);
    }

    elements.roomsTableBody.querySelectorAll("button[data-room-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const roomId = Number(button.dataset.roomId);
            const room = state.rooms.find((item) => item.id === roomId);

            if (room) {
                fillRoomForm(room);
            }
        });
    });
}

function fillRoomForm(room) {
    elements.roomIdInput.value = room.id;
    elements.roomNumberInput.value = room.room_number ?? "";
    elements.roomNameRuInput.value = room.name_ru ?? room.name ?? "";
    elements.roomNameEnInput.value = room.name_en ?? "";
    elements.roomCodeInput.value = room.code ?? "";
    elements.saveRoomButton.textContent = "Сохранить помещение";
}

function clearRoomForm() {
    elements.roomIdInput.value = "";
    elements.roomNumberInput.value = "";
    elements.roomNameRuInput.value = "";
    elements.roomNameEnInput.value = "";
    elements.roomCodeInput.value = "";
    elements.saveRoomButton.textContent = "Добавить помещение";
}

async function saveRoom() {
    if (!state.activeProjectId) {
        log("Сначала выберите проект");
        return;
    }

    const roomId = elements.roomIdInput.value.trim();
    const roomNumber = elements.roomNumberInput.value.trim();
    const nameRu = elements.roomNameRuInput.value.trim();
    const nameEn = elements.roomNameEnInput.value.trim();
    const code = elements.roomCodeInput.value.trim();

    if (!roomNumber || !nameRu || !code) {
        log("Заполните номер помещения, название RU и код");
        return;
    }

    const payload = {
        room_number: roomNumber,
        name: nameEn || nameRu,
        code,
        name_ru: nameRu,
        name_en: nameEn || null,
    };

    if (roomId) {
        await requestJson(`${api}/rooms/${roomId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        log(`Помещение обновлено: ${roomNumber} ${nameRu}`);
    } else {
        await requestJson(`${api}/projects/${state.activeProjectId}/rooms`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        log(`Помещение добавлено: ${roomNumber} ${nameRu}`);
    }

    clearRoomForm();
    await loadRooms();
}

async function loadLightingGroups() {
    if (!state.activeProjectId) {
        return;
    }

    state.lightingGroups = await requestJson(`${api}/projects/${state.activeProjectId}/lighting-groups`);
    renderLightingGroups();
}

function renderLightingGroups() {
    elements.lightingTableBody.innerHTML = "";

    for (const group of state.lightingGroups) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${escapeHtml(group.id)}</td>
            <td>${escapeHtml(group.room_number)} ${escapeHtml(group.room_name)}</td>
            <td>${escapeHtml(group.name)}</td>
            <td>${escapeHtml(group.code)}</td>
            <td>${escapeHtml(group.load_type)}</td>
            <td>${escapeHtml(group.quantity)}</td>
            <td>${escapeHtml(group.device_type)}</td>
            <td>${escapeHtml(group.device_address)}</td>
            <td>${escapeHtml(group.device_output)}</td>
            <td>
                <div class="table-actions">
                    <button type="button" data-lighting-edit-id="${escapeHtml(group.id)}" class="secondary">Редактировать</button>
                    <button type="button" data-lighting-delete-id="${escapeHtml(group.id)}" class="danger">Удалить</button>
                </div>
            </td>
        `;

        elements.lightingTableBody.appendChild(tr);
    }

    elements.lightingTableBody.querySelectorAll("button[data-lighting-edit-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const groupId = Number(button.dataset.lightingEditId);
            const group = state.lightingGroups.find((item) => item.id === groupId);

            if (group) {
                fillLightingForm(group);
            }
        });
    });

    elements.lightingTableBody.querySelectorAll("button[data-lighting-delete-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const groupId = Number(button.dataset.lightingDeleteId);
            deleteLightingGroup(groupId).catch((error) => log(error.message));
        });
    });
}

function fillLightingForm(group) {
    elements.lightingIdInput.value = group.id;
    elements.lightingRoomNumberInput.value = group.room_number ?? "";
    elements.lightingNameInput.value = group.name ?? "";
    elements.lightingCodeInput.value = group.code ?? "";
    elements.lightingLoadTypeInput.value = group.load_type ?? "RELAY";
    elements.lightingQuantityInput.value = group.quantity ?? 1;
    elements.lightingDeviceTypeInput.value = group.device_type ?? "";
    elements.lightingDeviceAddressInput.value = group.device_address ?? "";
    elements.lightingDeviceOutputInput.value = group.device_output ?? "";
    elements.lightingDimmerChannelInput.value = group.dimmer_channel ?? "";
    elements.saveLightingButton.textContent = "Сохранить группу света";
    switchTab("lighting");
}

function clearLightingForm() {
    elements.lightingIdInput.value = "";
    elements.lightingRoomNumberInput.value = "";
    elements.lightingNameInput.value = "";
    elements.lightingCodeInput.value = "";
    elements.lightingLoadTypeInput.value = "RELAY";
    elements.lightingQuantityInput.value = "1";
    elements.lightingDeviceTypeInput.value = "";
    elements.lightingDeviceAddressInput.value = "";
    elements.lightingDeviceOutputInput.value = "";
    elements.lightingDimmerChannelInput.value = "";
    elements.saveLightingButton.textContent = "Добавить группу света";
}

function buildLightingPayload() {
    const dimmerChannel = elements.lightingDimmerChannelInput.value.trim();

    return {
        room_number: elements.lightingRoomNumberInput.value.trim(),
        name: elements.lightingNameInput.value.trim(),
        code: elements.lightingCodeInput.value.trim(),
        load_type: elements.lightingLoadTypeInput.value,
        quantity: Number(elements.lightingQuantityInput.value || 1),
        device_type: elements.lightingDeviceTypeInput.value.trim() || null,
        device_address: elements.lightingDeviceAddressInput.value.trim() || null,
        device_output: elements.lightingDeviceOutputInput.value.trim() || null,
        dimmer_channel: dimmerChannel || null,
    };
}

async function saveLightingGroup() {
    if (!state.activeProjectId) {
        log("Сначала выберите проект");
        return;
    }

    const groupId = elements.lightingIdInput.value.trim();
    const payload = buildLightingPayload();

    if (!payload.room_number || !payload.name || !payload.code || !payload.load_type) {
        log("Заполните № помещения, название, код и тип нагрузки");
        return;
    }

    if (payload.quantity <= 0) {
        log("Количество должно быть больше 0");
        return;
    }

    if (groupId) {
        await requestJson(`${api}/lighting-groups/${groupId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        log(`Группа света обновлена: ${payload.room_number} ${payload.name}`);
    } else {
        await requestJson(`${api}/projects/${state.activeProjectId}/lighting-groups`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(payload),
        });

        log(`Группа света добавлена: ${payload.room_number} ${payload.name}`);
    }

    clearLightingForm();
    await loadLightingGroups();
}

async function deleteLightingGroup(groupId) {
    const confirmed = confirm(`Удалить группу света ID ${groupId}?`);

    if (!confirmed) {
        return;
    }

    await requestJson(`${api}/lighting-groups/${groupId}`, {
        method: "DELETE",
    });

    log(`Группа света удалена: ID ${groupId}`);
    await loadLightingGroups();
}

function downloadExport(type) {
    if (!state.activeProjectId) {
        log("Сначала выберите проект");
        return;
    }

    const urls = {
        "central-functions": `/projects/${state.activeProjectId}/central-functions-ets-csv-v1-download`,
        "rooms": `/projects/${state.activeProjectId}/rooms-ets-csv-v1-download`,
        "lighting": `/projects/${state.activeProjectId}/ets-lighting-csv-v1-download`,
        "mechanisms": `/projects/${state.activeProjectId}/mechanisms-ets-csv-v1-download`,
        "floor-heating": `/projects/${state.activeProjectId}/floor-heating-ets-csv-v1-download`,
        "climate": `/projects/${state.activeProjectId}/climate-ets-csv-v1-download`,
        "fans": `/projects/${state.activeProjectId}/fans-ets-csv-v1-download`,
    };

    const url = urls[type];

    if (!url) {
        log(`Неизвестный экспорт: ${type}`);
        return;
    }

    window.location.href = url;
    log(`Скачивание: ${type}`);
}

function bindEvents() {
    document.querySelectorAll(".tab-button").forEach((button) => {
        button.addEventListener("click", () => switchTab(button.dataset.tab));
    });

    elements.createProjectButton.addEventListener("click", () => {
        createProject().catch((error) => log(error.message));
    });

    elements.reloadButton.addEventListener("click", () => {
        init().catch((error) => log(error.message));
    });

    elements.projectSelect.addEventListener("change", async () => {
        state.activeProjectId = Number(elements.projectSelect.value);
        clearRoomForm();
        clearLightingForm();
        await loadRooms();
        await loadLightingGroups();
    });

    elements.saveRoomButton.addEventListener("click", () => {
        saveRoom().catch((error) => log(error.message));
    });

    elements.clearRoomFormButton.addEventListener("click", clearRoomForm);

    elements.saveLightingButton.addEventListener("click", () => {
        saveLightingGroup().catch((error) => log(error.message));
    });

    elements.clearLightingFormButton.addEventListener("click", clearLightingForm);

    document.querySelectorAll("button[data-export]").forEach((button) => {
        button.addEventListener("click", () => downloadExport(button.dataset.export));
    });
}

async function init() {
    await loadProjects();
    updateRoomNumberSelects();
    log("Интерфейс загружен");
}

attachRoomNumberDatalists();
bindEvents();
init().catch((error) => log(error.message));


function attachRoomNumberDatalists() {
    // Больше не используем datalist.
    // Поля помещений переведены на обычные select.
}

function updateRoomNumberDatalist() {
    // Больше не используем datalist.
    // Поля помещений переведены на обычные select.
}


function updateRoomNumberSelects() {
    const selectIds = [
        "lightingRoomNumberInput",
        "mechanismRoomNumberInput",
        "fanRoomNumberInput",
        "floorHeatingRoomNumberInput",
        "climateRoomNumberInput"
    ];

    for (const selectId of selectIds) {
        const select = document.getElementById(selectId);

        if (!select) {
            continue;
        }

        const previousValue = select.value;
        select.innerHTML = "";

        const emptyOption = document.createElement("option");
        emptyOption.value = "";
        emptyOption.textContent = "Выберите помещение";
        select.appendChild(emptyOption);

        for (const room of state.rooms) {
            const option = document.createElement("option");

            const roomNumber = String(room.room_number ?? "");
            const roomName = room.name_ru || room.name || room.code || "";

            option.value = roomNumber;
            option.textContent = roomName
                ? `${roomNumber} — ${roomName}`
                : roomNumber;

            select.appendChild(option);
        }

        if (previousValue) {
            select.value = previousValue;
        }
    }
}

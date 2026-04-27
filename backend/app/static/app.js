const api = "";

const state = {
    projects: [],
    rooms: [],
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

    logOutput: document.getElementById("logOutput"),
};

function log(message) {
    const time = new Date().toLocaleTimeString();
    elements.logOutput.textContent = `[${time}] ${message}\n` + elements.logOutput.textContent;
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${text}`);
    }

    return response.json();
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
    } else {
        state.activeProjectId = null;
        elements.roomsTableBody.innerHTML = "";
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
}

async function loadRooms() {
    if (!state.activeProjectId) {
        return;
    }

    state.rooms = await requestJson(`${api}/projects/${state.activeProjectId}/rooms`);
    renderRooms();
}

function renderRooms() {
    elements.roomsTableBody.innerHTML = "";

    for (const room of state.rooms) {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${room.id}</td>
            <td>${room.room_number ?? ""}</td>
            <td>${room.name_ru ?? ""}</td>
            <td>${room.name_en ?? ""}</td>
            <td>${room.code ?? ""}</td>
            <td>
                <button type="button" data-room-id="${room.id}" class="secondary">Редактировать</button>
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
    elements.createProjectButton.addEventListener("click", () => {
        createProject().catch((error) => log(error.message));
    });

    elements.reloadButton.addEventListener("click", () => {
        init().catch((error) => log(error.message));
    });

    elements.projectSelect.addEventListener("change", async () => {
        state.activeProjectId = Number(elements.projectSelect.value);
        clearRoomForm();
        await loadRooms();
    });

    elements.saveRoomButton.addEventListener("click", () => {
        saveRoom().catch((error) => log(error.message));
    });

    elements.clearRoomFormButton.addEventListener("click", clearRoomForm);

    document.querySelectorAll("button[data-export]").forEach((button) => {
        button.addEventListener("click", () => downloadExport(button.dataset.export));
    });
}

async function init() {
    await loadProjects();
    log("Интерфейс загружен");
}

bindEvents();
init().catch((error) => log(error.message));

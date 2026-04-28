const projectSummaryElements = {
    projectSelect: document.getElementById("projectSelect"),
    refreshButton: document.getElementById("refreshProjectSummaryButton"),
    status: document.getElementById("summaryStatus"),

    rooms: document.getElementById("summaryRoomsCount"),
    equipment: document.getElementById("summaryEquipmentCount"),
    lighting: document.getElementById("summaryLightingCount"),
    rgbwLighting: document.getElementById("summaryRgbwLightingCount"),
    mechanisms: document.getElementById("summaryMechanismsCount"),
    fans: document.getElementById("summaryFansCount"),
    socketsContactors: document.getElementById("summarySocketsContactorsCount"),
    floorHeating: document.getElementById("summaryFloorHeatingCount"),
    climate: document.getElementById("summaryClimateCount"),
};

function getActiveProjectIdForSummary() {
    const value = projectSummaryElements.projectSelect?.value;
    return value ? Number(value) : null;
}

function setSummaryValue(element, value) {
    if (element) {
        element.textContent = value;
    }
}

function setSummaryLoading() {
    setSummaryValue(projectSummaryElements.rooms, "…");
    setSummaryValue(projectSummaryElements.equipment, "…");
    setSummaryValue(projectSummaryElements.lighting, "…");
    setSummaryValue(projectSummaryElements.rgbwLighting, "…");
    setSummaryValue(projectSummaryElements.mechanisms, "…");
    setSummaryValue(projectSummaryElements.fans, "…");
    setSummaryValue(projectSummaryElements.socketsContactors, "…");
    setSummaryValue(projectSummaryElements.floorHeating, "…");
    setSummaryValue(projectSummaryElements.climate, "…");
}

function setSummaryEmpty() {
    setSummaryValue(projectSummaryElements.rooms, "—");
    setSummaryValue(projectSummaryElements.equipment, "—");
    setSummaryValue(projectSummaryElements.lighting, "—");
    setSummaryValue(projectSummaryElements.rgbwLighting, "—");
    setSummaryValue(projectSummaryElements.mechanisms, "—");
    setSummaryValue(projectSummaryElements.fans, "—");
    setSummaryValue(projectSummaryElements.socketsContactors, "—");
    setSummaryValue(projectSummaryElements.floorHeating, "—");
    setSummaryValue(projectSummaryElements.climate, "—");
}

async function fetchJson(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }

    return await response.json();
}

function isRgbwLightingGroup(item) {
    const loadType = String(
        item?.load_type ||
        item?.loadType ||
        item?.type ||
        ""
    ).trim().toUpperCase();

    return loadType === "RGBW";
}

async function refreshProjectSummary() {
    const projectId = getActiveProjectIdForSummary();

    if (!projectId) {
        setSummaryEmpty();

        if (projectSummaryElements.status) {
            projectSummaryElements.status.textContent = "Выберите проект";
        }

        return;
    }

    setSummaryLoading();

    if (projectSummaryElements.status) {
        projectSummaryElements.status.textContent = "Обновляем сводку...";
    }

    try {
        const [
            rooms,
            equipment,
            lightingGroups,
            mechanisms,
            fans,
            floorHeating,
            climate,
        ] = await Promise.all([
            fetchJson(`/projects/${projectId}/rooms`),
            fetchJson(`/projects/${projectId}/equipment`),
            fetchJson(`/projects/${projectId}/lighting-groups`),
            fetchJson(`/projects/${projectId}/mechanisms`),
            fetchJson(`/projects/${projectId}/fans`),
            fetchJson(`/projects/${projectId}/floor-heating`),
            fetchJson(`/projects/${projectId}/climate`),
        ]);

        const rgbwLightingGroups = lightingGroups.filter(isRgbwLightingGroup);
        const regularLightingGroups = lightingGroups.filter((item) => !isRgbwLightingGroup(item));

        setSummaryValue(projectSummaryElements.rooms, rooms.length);
        setSummaryValue(projectSummaryElements.equipment, equipment.length);
        setSummaryValue(projectSummaryElements.lighting, regularLightingGroups.length);
        setSummaryValue(projectSummaryElements.rgbwLighting, rgbwLightingGroups.length);
        setSummaryValue(projectSummaryElements.mechanisms, mechanisms.length);
        setSummaryValue(projectSummaryElements.fans, fans.length);
        setSummaryValue(projectSummaryElements.floorHeating, floorHeating.length);
        setSummaryValue(projectSummaryElements.climate, climate.length);

        const time = new Date().toLocaleTimeString();

        if (projectSummaryElements.status) {
            projectSummaryElements.status.textContent = `Обновлено: ${time}`;
        }
    } catch (error) {
        setSummaryEmpty();

        if (projectSummaryElements.status) {
            projectSummaryElements.status.textContent = `Ошибка сводки: ${error.message}`;
        }
    }
}

function bindProjectSummaryEvents() {
    if (projectSummaryElements.refreshButton) {
        projectSummaryElements.refreshButton.addEventListener("click", () => {
            refreshProjectSummary();
        });
    }

    if (projectSummaryElements.projectSelect) {
        projectSummaryElements.projectSelect.addEventListener("change", () => {
            setTimeout(refreshProjectSummary, 200);
        });
    }

    const reloadButton = document.getElementById("reloadButton");
    if (reloadButton) {
        reloadButton.addEventListener("click", () => {
            setTimeout(refreshProjectSummary, 800);
        });
    }

    const createProjectButton = document.getElementById("createProjectButton");
    if (createProjectButton) {
        createProjectButton.addEventListener("click", () => {
            setTimeout(refreshProjectSummary, 1000);
        });
    }

    document.querySelectorAll('.tab-button[data-tab="project"]').forEach((button) => {
        button.addEventListener("click", () => {
            setTimeout(refreshProjectSummary, 200);
        });
    });
}

bindProjectSummaryEvents();
setTimeout(refreshProjectSummary, 800);

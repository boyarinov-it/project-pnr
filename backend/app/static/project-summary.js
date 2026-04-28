const projectSummaryElements = {
    projectSelect: document.getElementById("projectSelect"),
    refreshButton: document.getElementById("refreshProjectSummaryButton"),
    status: document.getElementById("summaryStatus"),

    rooms: document.getElementById("summaryRoomsCount"),
    lighting: document.getElementById("summaryLightingCount"),
    mechanisms: document.getElementById("summaryMechanismsCount"),
    fans: document.getElementById("summaryFansCount"),
    floorHeating: document.getElementById("summaryFloorHeatingCount"),
    climate: document.getElementById("summaryClimateCount"),
};

function getActiveProjectIdForSummary() {
    const value = projectSummaryElements.projectSelect?.value;
    return value ? Number(value) : null;
}

function setSummaryLoading() {
    projectSummaryElements.rooms.textContent = "…";
    projectSummaryElements.lighting.textContent = "…";
    projectSummaryElements.mechanisms.textContent = "…";
    projectSummaryElements.fans.textContent = "…";
    projectSummaryElements.floorHeating.textContent = "…";
    projectSummaryElements.climate.textContent = "…";
}

function setSummaryEmpty() {
    projectSummaryElements.rooms.textContent = "—";
    projectSummaryElements.lighting.textContent = "—";
    projectSummaryElements.mechanisms.textContent = "—";
    projectSummaryElements.fans.textContent = "—";
    projectSummaryElements.floorHeating.textContent = "—";
    projectSummaryElements.climate.textContent = "—";
}

async function fetchSummaryCount(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    if (Array.isArray(data)) {
        return data.length;
    }

    return 0;
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

    const endpoints = {
        rooms: `/projects/${projectId}/rooms`,
        lighting: `/projects/${projectId}/lighting-groups`,
        mechanisms: `/projects/${projectId}/mechanisms`,
        fans: `/projects/${projectId}/fans`,
        floorHeating: `/projects/${projectId}/floor-heating`,
        climate: `/projects/${projectId}/climate`,
    };

    try {
        const [
            roomsCount,
            lightingCount,
            mechanismsCount,
            fansCount,
            floorHeatingCount,
            climateCount,
        ] = await Promise.all([
            fetchSummaryCount(endpoints.rooms),
            fetchSummaryCount(endpoints.lighting),
            fetchSummaryCount(endpoints.mechanisms),
            fetchSummaryCount(endpoints.fans),
            fetchSummaryCount(endpoints.floorHeating),
            fetchSummaryCount(endpoints.climate),
        ]);

        projectSummaryElements.rooms.textContent = roomsCount;
        projectSummaryElements.lighting.textContent = lightingCount;
        projectSummaryElements.mechanisms.textContent = mechanismsCount;
        projectSummaryElements.fans.textContent = fansCount;
        projectSummaryElements.floorHeating.textContent = floorHeatingCount;
        projectSummaryElements.climate.textContent = climateCount;

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

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.api.projects import router as projects_router
from app.api.rooms import router as rooms_router
from app.api.lighting_groups import router as lighting_groups_router
from app.api.mechanisms import router as mechanisms_router
from app.api.fans import router as fans_router
from app.api.floor_heating import router as floor_heating_router
from app.api.climate import router as climate_router

from app.api.mechanism_validation import router as mechanism_validation_router
from app.api.fan_validation import router as fan_validation_router
from app.api.floor_heating_validation import router as floor_heating_validation_router
from app.api.climate_validation import router as climate_validation_router

from app.api.ets_central_functions_v1 import router as ets_central_functions_v1_router
from app.api.ets_rooms_v1 import router as ets_rooms_v1_router
from app.api.ets_csv_v1 import router as ets_csv_v1_router
from app.api.ets_csv_v1_download import router as ets_csv_v1_download_router
from app.api.ets_rgbw_lighting_v1_download import router as ets_rgbw_lighting_v1_download_router
from app.api.ets_mechanisms_v1 import router as ets_mechanisms_v1_router
from app.api.ets_mechanisms_v1_download import router as ets_mechanisms_v1_download_router
from app.api.ets_fans_v1 import router as ets_fans_v1_router
from app.api.ets_floor_heating_v1 import router as ets_floor_heating_v1_router
from app.api.ets_climate_v1 import router as ets_climate_v1_router

# Service/internal routers.
# Они остаются в backend, но скрыты из Swagger UI.
from app.api.standards import router as standards_router
from app.api.lighting_validation import router as lighting_validation_router

# Legacy/internal routers.
# Они остаются доступными в backend, но скрыты из Swagger UI.
from app.api.knx_preview import router as knx_preview_router
from app.api.ets_preview import router as ets_preview_router
from app.api.csv_preview import router as csv_preview_router
from app.api.project_csv_preview import router as project_csv_preview_router
from app.api.project_csv_download import router as project_csv_download_router
from app.api.validation import router as validation_router
from app.api.export_jobs import router as export_jobs_router
from app.api.export_files import router as export_files_router
from app.api.equipment import router as equipment_router
from app.api.sockets_contactors import router as sockets_contactors_router
from app.api.sockets_contactors_ets_csv_v1_download import router as sockets_contactors_ets_csv_v1_download_router

from app.core.config import settings
from app.db.session import engine


tags_metadata = [
    {"name": "projects", "description": "Проекты"},
    {"name": "rooms", "description": "Экспликация помещений"},
    {"name": "lighting-groups", "description": "Освещение"},
    {"name": "mechanisms", "description": "Механизмы / шторы"},
    {"name": "fans", "description": "Вытяжные вентиляторы"},
    {"name": "floor-heating", "description": "Теплый пол"},
    {"name": "climate", "description": "Климат"},

    {"name": "central-functions-ets-csv-v1", "description": "ETS CSV: 0/0 Центральные функции"},
    {"name": "rooms-ets-csv-v1", "description": "ETS CSV: 0/1 Помещения"},
    {"name": "ets-csv-v1", "description": "ETS CSV: 1 Освещение"},
    {"name": "mechanisms-ets-csv-v1", "description": "ETS CSV: 2 Механизмы"},
    {"name": "fans-ets-csv-v1", "description": "ETS CSV: 8 Вытяжные вентиляторы"},
    {"name": "floor-heating-ets-csv-v1", "description": "ETS CSV: 3 Теплый пол"},
    {"name": "climate-ets-csv-v1", "description": "ETS CSV: 5 Климат контроль"},
]


app = FastAPI(
    title=settings.app_name,
    openapi_tags=tags_metadata,
)

# 1. Main project data
app.include_router(projects_router)
app.include_router(rooms_router)
app.include_router(equipment_router)
app.include_router(sockets_contactors_ets_csv_v1_download_router)
app.include_router(sockets_contactors_router)
app.include_router(lighting_groups_router)
app.include_router(mechanisms_router)
app.include_router(fans_router)
app.include_router(floor_heating_router)
app.include_router(climate_router)

# 2. Validation endpoints
app.include_router(mechanism_validation_router)
app.include_router(fan_validation_router)
app.include_router(floor_heating_validation_router)
app.include_router(climate_validation_router)

# 3. ETS CSV exports
app.include_router(ets_central_functions_v1_router)
app.include_router(ets_rooms_v1_router)
app.include_router(ets_csv_v1_router)
app.include_router(ets_csv_v1_download_router)
app.include_router(ets_rgbw_lighting_v1_download_router)
app.include_router(ets_mechanisms_v1_router)
app.include_router(ets_mechanisms_v1_download_router)
app.include_router(ets_fans_v1_router)
app.include_router(ets_floor_heating_v1_router)
app.include_router(ets_climate_v1_router)

# Hidden service/internal API
app.include_router(standards_router, include_in_schema=False)
app.include_router(lighting_validation_router, include_in_schema=False)

# Hidden legacy/internal API
app.include_router(knx_preview_router, include_in_schema=False)
app.include_router(ets_preview_router, include_in_schema=False)
app.include_router(csv_preview_router, include_in_schema=False)
app.include_router(project_csv_preview_router, include_in_schema=False)
app.include_router(project_csv_download_router, include_in_schema=False)
app.include_router(validation_router, include_in_schema=False)
app.include_router(export_jobs_router, include_in_schema=False)
app.include_router(export_files_router, include_in_schema=False)


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@app.get("/health/db", include_in_schema=False)
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "ok", "database": "connected"}
# Frontend MVP
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

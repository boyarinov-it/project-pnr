from fastapi import FastAPI
from sqlalchemy import text

from app.api.projects import router as projects_router
from app.api.rooms import router as rooms_router
from app.api.lighting_groups import router as lighting_groups_router
from app.api.mechanisms import router as mechanisms_router
from app.api.floor_heating import router as floor_heating_router
from app.api.floor_heating_validation import router as floor_heating_validation_router
from app.api.ets_mechanisms_v1 import router as ets_mechanisms_v1_router
from app.api.ets_mechanisms_v1_download import router as ets_mechanisms_v1_download_router
from app.api.mechanism_validation import router as mechanism_validation_router

from app.api.standards import router as standards_router
from app.api.lighting_validation import router as lighting_validation_router
from app.api.ets_csv_v1 import router as ets_csv_v1_router

# Legacy / internal routers.
# They remain available in backend, but are hidden from Swagger UI.
from app.api.knx_preview import router as knx_preview_router
from app.api.ets_preview import router as ets_preview_router
from app.api.csv_preview import router as csv_preview_router
from app.api.project_csv_preview import router as project_csv_preview_router
from app.api.project_csv_download import router as project_csv_download_router
from app.api.validation import router as validation_router
from app.api.export_jobs import router as export_jobs_router
from app.api.export_files import router as export_files_router

from app.core.config import settings
from app.db.session import engine


app = FastAPI(title=settings.app_name)

# Visible MVP API
app.include_router(projects_router)
app.include_router(rooms_router)
app.include_router(lighting_groups_router)
app.include_router(mechanisms_router)
app.include_router(floor_heating_router)
app.include_router(floor_heating_validation_router)
app.include_router(ets_mechanisms_v1_router)
app.include_router(ets_mechanisms_v1_download_router)
app.include_router(mechanism_validation_router)
app.include_router(standards_router)
app.include_router(lighting_validation_router)
app.include_router(ets_csv_v1_router)

# Hidden legacy/internal API
app.include_router(knx_preview_router, include_in_schema=False)
app.include_router(ets_preview_router, include_in_schema=False)
app.include_router(csv_preview_router, include_in_schema=False)
app.include_router(project_csv_preview_router, include_in_schema=False)
app.include_router(project_csv_download_router, include_in_schema=False)
app.include_router(validation_router, include_in_schema=False)
app.include_router(export_jobs_router, include_in_schema=False)
app.include_router(export_files_router, include_in_schema=False)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@app.get("/health/db")
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}





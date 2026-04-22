from fastapi import FastAPI
from sqlalchemy import text

from app.api.projects import router as projects_router
from app.api.rooms import router as rooms_router
from app.api.lighting_groups import router as lighting_groups_router
from app.api.knx_preview import router as knx_preview_router
from app.api.ets_preview import router as ets_preview_router
from app.api.csv_preview import router as csv_preview_router
from app.api.project_csv_preview import router as project_csv_preview_router
from app.api.project_csv_download import router as project_csv_download_router
from app.api.validation import router as validation_router
from app.core.config import settings
from app.db.session import engine

app = FastAPI(title=settings.app_name)

app.include_router(projects_router)
app.include_router(rooms_router)
app.include_router(lighting_groups_router)
app.include_router(knx_preview_router)
app.include_router(ets_preview_router)
app.include_router(csv_preview_router)
app.include_router(project_csv_preview_router)
app.include_router(project_csv_download_router)
app.include_router(validation_router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@app.get("/health/db")
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}

from fastapi import FastAPI
from sqlalchemy import text

from app.api.projects import router as projects_router
from app.api.rooms import router as rooms_router
from app.core.config import settings
from app.db.session import engine

app = FastAPI(title=settings.app_name)

app.include_router(projects_router)
app.include_router(rooms_router)

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}

@app.get("/health/db")
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}

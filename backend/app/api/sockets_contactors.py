from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.socket_contactor import SocketContactor
from app.schemas.socket_contactor import (
    SocketContactorCreate,
    SocketContactorRead,
    SocketContactorUpdate,
)


router = APIRouter(tags=["sockets-contactors"])


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None

    value = value.strip()
    return value or None


def normalize_required(value: str | None, field_name: str) -> str:
    value = (value or "").strip()

    if not value:
        raise HTTPException(status_code=422, detail=f"{field_name} is required")

    return value


def get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.get("/projects/{project_id}/sockets-contactors", response_model=list[SocketContactorRead])
def list_sockets_contactors(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)

    return (
        db.query(SocketContactor)
        .filter(SocketContactor.project_id == project_id)
        .order_by(SocketContactor.id.asc())
        .all()
    )


@router.post("/projects/{project_id}/sockets-contactors", response_model=SocketContactorRead)
def create_socket_contactor(
    project_id: int,
    payload: SocketContactorCreate,
    db: Session = Depends(get_db),
):
    get_project_or_404(db, project_id)

    item = SocketContactor(
        project_id=project_id,
        room_number=normalize_text(payload.room_number),
        code=normalize_required(payload.code, "Code"),
        name=normalize_required(payload.name, "Name"),
        load_type=normalize_required(payload.load_type, "Load type").upper(),
        device_type=normalize_text(payload.device_type),
        device_address=normalize_text(payload.device_address),
        device_output=normalize_text(payload.device_output),
        description=normalize_text(payload.description),
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.put("/sockets-contactors/{item_id}", response_model=SocketContactorRead)
def update_socket_contactor(
    item_id: int,
    payload: SocketContactorUpdate,
    db: Session = Depends(get_db),
):
    item = db.query(SocketContactor).filter(SocketContactor.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Socket/contactor not found")

    item.room_number = normalize_text(payload.room_number)
    item.code = normalize_required(payload.code, "Code")
    item.name = normalize_required(payload.name, "Name")
    item.load_type = normalize_required(payload.load_type, "Load type").upper()
    item.device_type = normalize_text(payload.device_type)
    item.device_address = normalize_text(payload.device_address)
    item.device_output = normalize_text(payload.device_output)
    item.description = normalize_text(payload.description)

    db.commit()
    db.refresh(item)

    return item


@router.delete("/sockets-contactors/{item_id}")
def delete_socket_contactor(item_id: int, db: Session = Depends(get_db)):
    item = db.query(SocketContactor).filter(SocketContactor.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Socket/contactor not found")

    db.delete(item)
    db.commit()

    return {"status": "deleted", "id": item_id}

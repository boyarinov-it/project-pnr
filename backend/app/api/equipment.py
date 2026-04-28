from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.equipment import Equipment
from app.models.project import Project
from app.schemas.equipment import EquipmentCreate, EquipmentRead, EquipmentUpdate


router = APIRouter(tags=["equipment"])


def get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None

    value = value.strip()

    return value or None


def get_duplicate_address(
    db: Session,
    project_id: int,
    individual_address: str,
    exclude_id: int | None = None,
) -> Equipment | None:
    query = (
        db.query(Equipment)
        .filter(Equipment.project_id == project_id)
        .filter(Equipment.individual_address == individual_address)
    )

    if exclude_id is not None:
        query = query.filter(Equipment.id != exclude_id)

    return query.first()


@router.post("/projects/{project_id}/equipment", response_model=EquipmentRead)
def create_equipment(
    project_id: int,
    payload: EquipmentCreate,
    db: Session = Depends(get_db),
):
    get_project_or_404(db, project_id)

    name = payload.name.strip()
    individual_address = payload.individual_address.strip()

    if not name:
        raise HTTPException(status_code=422, detail="Equipment name is required")

    if not individual_address:
        raise HTTPException(status_code=422, detail="Individual address is required")

    duplicate = get_duplicate_address(db, project_id, individual_address)

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail=f"Equipment address already exists: {individual_address}",
        )

    equipment = Equipment(
        project_id=project_id,
        room_number=normalize_text(payload.room_number),
        name=name,
        equipment_type=normalize_text(payload.equipment_type),
        individual_address=individual_address,
        description=normalize_text(payload.description),
    )

    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    return equipment


@router.get("/projects/{project_id}/equipment", response_model=list[EquipmentRead])
def list_equipment(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)

    return (
        db.query(Equipment)
        .filter(Equipment.project_id == project_id)
        .order_by(Equipment.individual_address.asc(), Equipment.id.asc())
        .all()
    )


@router.put("/equipment/{equipment_id}", response_model=EquipmentRead)
def update_equipment(
    equipment_id: int,
    payload: EquipmentUpdate,
    db: Session = Depends(get_db),
):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    name = payload.name.strip()
    individual_address = payload.individual_address.strip()

    if not name:
        raise HTTPException(status_code=422, detail="Equipment name is required")

    if not individual_address:
        raise HTTPException(status_code=422, detail="Individual address is required")

    duplicate = get_duplicate_address(
        db=db,
        project_id=equipment.project_id,
        individual_address=individual_address,
        exclude_id=equipment.id,
    )

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail=f"Equipment address already exists: {individual_address}",
        )

    equipment.room_number = normalize_text(payload.room_number)
    equipment.name = name
    equipment.equipment_type = normalize_text(payload.equipment_type)
    equipment.individual_address = individual_address
    equipment.description = normalize_text(payload.description)

    db.commit()
    db.refresh(equipment)

    return equipment


@router.delete("/equipment/{equipment_id}")
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    db.delete(equipment)
    db.commit()

    return {"status": "deleted", "equipment_id": equipment_id}

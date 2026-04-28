from pydantic import BaseModel, ConfigDict


class EquipmentCreate(BaseModel):
    room_number: str | None = None
    name: str
    equipment_type: str | None = None
    individual_address: str
    description: str | None = None


class EquipmentUpdate(BaseModel):
    room_number: str | None = None
    name: str
    equipment_type: str | None = None
    individual_address: str
    description: str | None = None


class EquipmentRead(BaseModel):
    id: int
    project_id: int
    room_number: str | None = None
    name: str
    equipment_type: str | None = None
    individual_address: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict

class LightingGroupCreate(BaseModel):
    room_id: int
    name: str
    code: str
    load_type: str
    quantity: int

class LightingGroupRead(BaseModel):
    id: int
    project_id: int
    room_id: int
    name: str
    code: str
    load_type: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)

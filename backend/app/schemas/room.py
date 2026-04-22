from pydantic import BaseModel, ConfigDict

class RoomCreate(BaseModel):
    name: str
    code: str

class RoomRead(BaseModel):
    id: int
    project_id: int
    name: str
    code: str

    model_config = ConfigDict(from_attributes=True)

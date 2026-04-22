from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    code: str


class ProjectRead(BaseModel):
    id: int
    name: str
    code: str

    model_config = ConfigDict(from_attributes=True)

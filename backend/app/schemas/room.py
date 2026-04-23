from pydantic import BaseModel, ConfigDict


class RoomCreate(BaseModel):
    name: str
    code: str
    name_ru: str | None = None
    name_en: str | None = None


class RoomRead(BaseModel):
    id: int
    project_id: int
    name: str
    code: str
    name_ru: str | None = None
    name_en: str | None = None

    model_config = ConfigDict(from_attributes=True)

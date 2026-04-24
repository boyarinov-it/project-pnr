from pydantic import BaseModel, ConfigDict


class FanCreate(BaseModel):
    room_number: str
    name: str
    code: str
    quantity: int = 1
    device_type: str | None = None
    device_address: str | None = None
    device_channel: str | None = None


class FanUpdate(BaseModel):
    room_number: str
    name: str
    code: str
    quantity: int = 1
    device_type: str | None = None
    device_address: str | None = None
    device_channel: str | None = None


class FanRead(BaseModel):
    id: int
    project_id: int
    room_id: int
    room_number: str
    room_name: str
    display_name: str
    name: str
    code: str
    quantity: int
    device_type: str | None = None
    device_address: str | None = None
    device_channel: str | None = None

    model_config = ConfigDict(from_attributes=True)

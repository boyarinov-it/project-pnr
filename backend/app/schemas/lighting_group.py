from pydantic import BaseModel, ConfigDict


class LightingGroupCreate(BaseModel):
    room_id: int
    name: str
    code: str
    load_type: str
    quantity: int
    device_type: str | None = None
    device_address: str | None = None
    device_output: str | None = None
    dimmer_channel: str | None = None


class LightingGroupRead(BaseModel):
    id: int
    project_id: int
    room_id: int
    name: str
    code: str
    load_type: str
    quantity: int
    device_type: str | None = None
    device_address: str | None = None
    device_output: str | None = None
    dimmer_channel: str | None = None

    model_config = ConfigDict(from_attributes=True)

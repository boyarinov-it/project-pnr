from pydantic import BaseModel, ConfigDict


class ClimateCreate(BaseModel):
    room_number: str
    name: str
    code: str
    climate_type: str
    quantity: int = 1
    device_type: str | None = None
    device_address: str | None = None
    device_channel: str | None = None
    gateway_address: str | None = None
    external_id: str | None = None


class ClimateUpdate(BaseModel):
    room_number: str
    name: str
    code: str
    climate_type: str
    quantity: int = 1
    device_type: str | None = None
    device_address: str | None = None
    device_channel: str | None = None
    gateway_address: str | None = None
    external_id: str | None = None


class ClimateRead(BaseModel):
    id: int
    project_id: int
    room_id: int
    room_number: str
    room_name: str
    display_name: str
    name: str
    code: str
    climate_type: str
    quantity: int
    device_type: str | None = None
    device_address: str | None = None
    device_channel: str | None = None
    gateway_address: str | None = None
    external_id: str | None = None

    model_config = ConfigDict(from_attributes=True)

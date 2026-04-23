from pydantic import BaseModel


class LightingGroupCreate(BaseModel):
    room_number: str
    name: str
    code: str
    load_type: str
    quantity: int
    device_type: str
    device_address: str
    device_output: str
    dimmer_channel: str | None = None


class LightingGroupRead(BaseModel):
    id: int
    project_id: int
    room_id: int
    room_number: str
    room_name: str
    name: str
    code: str
    load_type: str
    quantity: int
    device_type: str
    device_address: str
    device_output: str
    dimmer_channel: str | None = None
    display_name: str
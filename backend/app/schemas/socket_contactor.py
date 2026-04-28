from pydantic import BaseModel, ConfigDict


class SocketContactorCreate(BaseModel):
    room_number: str | None = None
    code: str
    name: str
    load_type: str = "SOCKET"
    device_type: str | None = None
    device_address: str | None = None
    device_output: str | None = None
    description: str | None = None


class SocketContactorUpdate(BaseModel):
    room_number: str | None = None
    code: str
    name: str
    load_type: str = "SOCKET"
    device_type: str | None = None
    device_address: str | None = None
    device_output: str | None = None
    description: str | None = None


class SocketContactorRead(BaseModel):
    id: int
    project_id: int
    room_number: str | None = None
    code: str
    name: str
    load_type: str
    device_type: str | None = None
    device_address: str | None = None
    device_output: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

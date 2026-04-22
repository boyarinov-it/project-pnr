from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExportJobRead(BaseModel):
    id: int
    project_id: int
    export_type: str
    status: str
    filename: str
    checksum: str
    validation_snapshot: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExportFileRead(BaseModel):
    id: int
    export_job_id: int
    filename: str
    storage_path: str
    checksum: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

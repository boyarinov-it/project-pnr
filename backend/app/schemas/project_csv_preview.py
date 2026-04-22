from pydantic import BaseModel


class ProjectCsvPreview(BaseModel):
    project_id: int
    project_name: str
    filename: str
    content: str

from pydantic import BaseModel


class LightingGroupCsvPreview(BaseModel):
    lighting_group_id: int
    lighting_group_name: str
    filename: str
    content: str

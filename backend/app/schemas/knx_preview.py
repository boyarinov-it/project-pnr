from pydantic import BaseModel


class KnxObjectPreview(BaseModel):
    function: str
    name: str
    datapoint_type: str


class LightingGroupKnxPreview(BaseModel):
    lighting_group_id: int
    lighting_group_name: str
    objects: list[KnxObjectPreview]

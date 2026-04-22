from pydantic import BaseModel


class EtsGroupAddressRowPreview(BaseModel):
    group_address: str
    name: str
    datapoint_type: str
    function: str


class LightingGroupEtsPreview(BaseModel):
    lighting_group_id: int
    lighting_group_name: str
    rows: list[EtsGroupAddressRowPreview]

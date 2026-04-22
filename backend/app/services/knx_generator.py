from app.models.lighting_group import LightingGroup
from app.schemas.knx_preview import KnxObjectPreview, LightingGroupKnxPreview


def build_lighting_group_knx_preview(group: LightingGroup) -> LightingGroupKnxPreview:
    base_name = group.name

    objects = [
        KnxObjectPreview(function="switch", name=f"{base_name} Вкл/Выкл", datapoint_type="DPST-1-1"),
        KnxObjectPreview(function="dim_relative", name=f"{base_name} Диммирование относительное", datapoint_type="DPST-3-7"),
        KnxObjectPreview(function="brightness_percent", name=f"{base_name} Яркость %", datapoint_type="DPST-5-1"),
        KnxObjectPreview(function="status_switch", name=f"{base_name} Статус Вкл/Выкл", datapoint_type="DPST-1-1"),
        KnxObjectPreview(function="status_brightness_percent", name=f"{base_name} Статус Яркость %", datapoint_type="DPST-5-1"),
    ]

    return LightingGroupKnxPreview(
        lighting_group_id=group.id,
        lighting_group_name=group.name,
        objects=objects,
    )

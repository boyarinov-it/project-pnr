from app.models.lighting_group import LightingGroup
from app.schemas.ets_preview import EtsGroupAddressRowPreview, LightingGroupEtsPreview
from app.services.knx_generator import build_lighting_group_knx_preview


FUNCTION_DESCRIPTIONS = {
    "switch": "Команда включения/выключения",
    "dim_relative": "Относительное диммирование",
    "brightness_percent": "Абсолютная яркость в процентах",
    "status_switch": "Статус включения/выключения",
    "status_brightness_percent": "Статус яркости в процентах",
}


def build_lighting_group_ets_preview(group: LightingGroup) -> LightingGroupEtsPreview:
    knx_preview = build_lighting_group_knx_preview(group)

    rows = []
    for obj in knx_preview.objects:
        rows.append(
            EtsGroupAddressRowPreview(
                group_address=obj.group_address,
                name=obj.name,
                datapoint_type=obj.datapoint_type,
                function=obj.function,
                description=FUNCTION_DESCRIPTIONS.get(obj.function, ""),
            )
        )

    return LightingGroupEtsPreview(
        lighting_group_id=group.id,
        lighting_group_name=group.name,
        rows=rows,
    )

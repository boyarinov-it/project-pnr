from app.core.standard_profile import STANDARD_PROFILE
from app.models.lighting_group import LightingGroup
from app.schemas.knx_preview import KnxObjectPreview, LightingGroupKnxPreview
from app.services.group_address_engine import build_lighting_group_address
from app.services.naming_engine import build_lighting_object_name


def build_lighting_group_knx_preview(group: LightingGroup) -> LightingGroupKnxPreview:
    function_rules = STANDARD_PROFILE["lighting"]["functions"]

    objects = []

    for item in function_rules:
        objects.append(
            KnxObjectPreview(
                function=item["function"],
                name=build_lighting_object_name(group, item["suffix"]),
                datapoint_type=item["datapoint_type"],
                group_address=build_lighting_group_address(group, item["address_offset"]),
            )
        )

    return LightingGroupKnxPreview(
        lighting_group_id=group.id,
        lighting_group_name=group.name,
        objects=objects,
    )

from app.core.standard_profile import STANDARD_PROFILE
from app.models.lighting_group import LightingGroup
from app.schemas.knx_preview import KnxObjectPreview, LightingGroupKnxPreview


def build_lighting_group_knx_preview(group: LightingGroup) -> LightingGroupKnxPreview:
    base_name = group.name
    lighting_profile = STANDARD_PROFILE["lighting"]
    function_rules = lighting_profile["functions"]

    base_subgroup = (group.id - 1) * len(function_rules) + 1
    main_group = lighting_profile["main_group"]
    middle_group = lighting_profile["middle_group"]

    objects = []

    for item in function_rules:
        objects.append(
            KnxObjectPreview(
                function=item["function"],
                name=f"{base_name} {item['suffix']}",
                datapoint_type=item["datapoint_type"],
                group_address=f"{main_group}/{middle_group}/{base_subgroup + item['address_offset']}",
            )
        )

    return LightingGroupKnxPreview(
        lighting_group_id=group.id,
        lighting_group_name=group.name,
        objects=objects,
    )

from app.models.lighting_group import LightingGroup
from app.rules.lighting_profile import LIGHTING_KNX_PROFILE
from app.schemas.knx_preview import KnxObjectPreview, LightingGroupKnxPreview


def build_lighting_group_knx_preview(group: LightingGroup) -> LightingGroupKnxPreview:
    base_name = group.name
    base_subgroup = (group.id - 1) * len(LIGHTING_KNX_PROFILE) + 1

    objects = []

    for item in LIGHTING_KNX_PROFILE:
        objects.append(
            KnxObjectPreview(
                function=item["function"],
                name=f"{base_name} {item['suffix']}",
                datapoint_type=item["datapoint_type"],
                group_address=f"1/1/{base_subgroup + item['address_offset']}",
            )
        )

    return LightingGroupKnxPreview(
        lighting_group_id=group.id,
        lighting_group_name=group.name,
        objects=objects,
    )

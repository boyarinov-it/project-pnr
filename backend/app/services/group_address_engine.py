from app.core.standard_profile import STANDARD_PROFILE
from app.models.lighting_group import LightingGroup


def build_lighting_group_address(group: LightingGroup, address_offset: int) -> str:
    addressing = STANDARD_PROFILE["lighting"]["addressing"]

    main_group = addressing["main_group"]
    middle_group = addressing["middle_group"]
    objects_per_group = addressing["objects_per_group"]
    start_subgroup = addressing["start_subgroup"]

    base_subgroup = start_subgroup + ((group.id - 1) * objects_per_group)

    return f"{main_group}/{middle_group}/{base_subgroup + address_offset}"

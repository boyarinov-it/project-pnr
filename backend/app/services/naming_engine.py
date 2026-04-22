from app.core.standard_profile import STANDARD_PROFILE
from app.models.lighting_group import LightingGroup


def build_lighting_object_name(group: LightingGroup, suffix: str) -> str:
    pattern = STANDARD_PROFILE["lighting"]["naming_pattern"]
    room_name = group.room.name if group.room else ""
    return pattern.format(
        room_name=room_name,
        group_name=group.name,
        suffix=suffix,
    ).strip()

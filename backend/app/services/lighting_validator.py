from dataclasses import dataclass

from app.rules.lighting_profile import LIGHTING_ETS_PROFILE


@dataclass
class ValidationIssue:
    level: str
    code: str
    message: str
    entity_id: int | None = None


def validate_lighting_groups_for_export(project) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    required_fields = LIGHTING_ETS_PROFILE["validation"]["required_fields"]

    for group in project.lighting_groups:
        if "group.code" in required_fields:
            if not group.code:
                issues.append(ValidationIssue("error", "missing_group_code", "Lighting group code is missing", group.id))
            elif LIGHTING_ETS_PROFILE["validation"]["code_must_be_numeric"] and not str(group.code).isdigit():
                issues.append(ValidationIssue("error", "invalid_group_code", "Lighting group code must be numeric", group.id))

        if "group.name" in required_fields and not group.name:
            issues.append(ValidationIssue("error", "missing_group_name", "Lighting group name is missing", group.id))

        if "room.code" in required_fields:
            if not group.room or not group.room.code:
                issues.append(ValidationIssue("error", "missing_room_code", "Room code is missing", group.id))

        if "load_type" in required_fields and not group.load_type:
            issues.append(ValidationIssue("error", "missing_load_type", "Load type is missing", group.id))

        if "device_type" in required_fields and not group.device_type:
            issues.append(ValidationIssue("error", "missing_device_type", "Device type is missing", group.id))

        if "device_address" in required_fields and not group.device_address:
            issues.append(ValidationIssue("error", "missing_device_address", "Device address is missing", group.id))

        if "device_output" in required_fields and not group.device_output:
            issues.append(ValidationIssue("error", "missing_device_output", "Device output is missing", group.id))

    return issues

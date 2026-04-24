from dataclasses import dataclass

from app.models.floor_heating import FloorHeating


@dataclass
class FloorHeatingValidationIssue:
    level: str
    code: str
    message: str
    entity_id: int


def validate_floor_heating_for_export(project) -> list[FloorHeatingValidationIssue]:
    issues: list[FloorHeatingValidationIssue] = []

    for item in project.floor_heating:
        issues.extend(validate_floor_heating_item(item))

    return issues


def validate_floor_heating_item(item: FloorHeating) -> list[FloorHeatingValidationIssue]:
    issues: list[FloorHeatingValidationIssue] = []

    if not str(item.code or "").strip():
        issues.append(
            FloorHeatingValidationIssue(
                level="error",
                code="missing_floor_heating_code",
                message="Floor heating code is missing",
                entity_id=item.id,
            )
        )

    if not str(item.name or "").strip():
        issues.append(
            FloorHeatingValidationIssue(
                level="error",
                code="missing_floor_heating_name",
                message="Floor heating name is missing",
                entity_id=item.id,
            )
        )

    if not str(item.thermostat_type or "").strip():
        issues.append(
            FloorHeatingValidationIssue(
                level="error",
                code="missing_thermostat_type",
                message="Thermostat type is missing",
                entity_id=item.id,
            )
        )

    if item.quantity is None or item.quantity <= 0:
        issues.append(
            FloorHeatingValidationIssue(
                level="error",
                code="invalid_quantity",
                message="Floor heating quantity must be greater than zero",
                entity_id=item.id,
            )
        )

    if not str(item.device_type or "").strip():
        issues.append(
            FloorHeatingValidationIssue(
                level="error",
                code="missing_device_type",
                message="Device type is missing",
                entity_id=item.id,
            )
        )

    if not str(item.device_address or "").strip():
        issues.append(
            FloorHeatingValidationIssue(
                level="error",
                code="missing_device_address",
                message="Device address is missing",
                entity_id=item.id,
            )
        )

    if not str(item.device_channel or "").strip():
        issues.append(
            FloorHeatingValidationIssue(
                level="error",
                code="missing_device_channel",
                message="Device channel is missing",
                entity_id=item.id,
            )
        )

    return issues

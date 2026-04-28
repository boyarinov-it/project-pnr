from dataclasses import dataclass

from app.models.climate import Climate


@dataclass
class ClimateValidationIssue:
    level: str
    code: str
    message: str
    entity_id: int


def validate_climate_for_export(project) -> list[ClimateValidationIssue]:
    issues: list[ClimateValidationIssue] = []

    for item in project.climate:
        issues.extend(validate_climate_item(item))

    return issues


def validate_climate_item(item: Climate) -> list[ClimateValidationIssue]:
    issues: list[ClimateValidationIssue] = []

    if not str(item.code or "").strip():
        issues.append(
            ClimateValidationIssue(
                level="error",
                code="missing_climate_code",
                message="Climate code is missing",
                entity_id=item.id,
            )
        )

    if not str(item.name or "").strip():
        issues.append(
            ClimateValidationIssue(
                level="error",
                code="missing_climate_name",
                message="Climate name is missing",
                entity_id=item.id,
            )
        )

    if not str(item.climate_type or "").strip():
        issues.append(
            ClimateValidationIssue(
                level="error",
                code="missing_climate_type",
                message="Climate type is missing",
                entity_id=item.id,
            )
        )

    if item.quantity is None or item.quantity <= 0:
        issues.append(
            ClimateValidationIssue(
                level="error",
                code="invalid_quantity",
                message="Climate quantity must be greater than zero",
                entity_id=item.id,
            )
        )

    if not str(item.device_type or "").strip():
        issues.append(
            ClimateValidationIssue(
                level="warning",
                code="missing_device_type",
                message="Device type is missing",
                entity_id=item.id,
            )
        )

    if not str(item.device_address or "").strip():
        issues.append(
            ClimateValidationIssue(
                level="warning",
                code="missing_device_address",
                message="Device address is missing",
                entity_id=item.id,
            )
        )

    if not str(item.device_channel or "").strip():
        issues.append(
            ClimateValidationIssue(
                level="warning",
                code="missing_device_channel",
                message="Device channel is missing",
                entity_id=item.id,
            )
        )

    return issues

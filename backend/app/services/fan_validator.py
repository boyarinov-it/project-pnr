from dataclasses import dataclass

from app.models.fan import Fan


@dataclass
class FanValidationIssue:
    level: str
    code: str
    message: str
    entity_id: int


def validate_fans_for_export(project) -> list[FanValidationIssue]:
    issues: list[FanValidationIssue] = []

    for fan in project.fans:
        issues.extend(validate_fan(fan))

    return issues


def validate_fan(fan: Fan) -> list[FanValidationIssue]:
    issues: list[FanValidationIssue] = []

    if not str(fan.code or "").strip():
        issues.append(
            FanValidationIssue(
                level="error",
                code="missing_fan_code",
                message="Fan code is missing",
                entity_id=fan.id,
            )
        )

    if not str(fan.name or "").strip():
        issues.append(
            FanValidationIssue(
                level="error",
                code="missing_fan_name",
                message="Fan name is missing",
                entity_id=fan.id,
            )
        )

    if fan.quantity is None or fan.quantity <= 0:
        issues.append(
            FanValidationIssue(
                level="error",
                code="invalid_quantity",
                message="Fan quantity must be greater than zero",
                entity_id=fan.id,
            )
        )

    if not str(fan.device_type or "").strip():
        issues.append(
            FanValidationIssue(
                level="error",
                code="missing_device_type",
                message="Device type is missing",
                entity_id=fan.id,
            )
        )

    if not str(fan.device_address or "").strip():
        issues.append(
            FanValidationIssue(
                level="error",
                code="missing_device_address",
                message="Device address is missing",
                entity_id=fan.id,
            )
        )

    if not str(fan.device_channel or "").strip():
        issues.append(
            FanValidationIssue(
                level="error",
                code="missing_device_channel",
                message="Device channel is missing",
                entity_id=fan.id,
            )
        )

    return issues

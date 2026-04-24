from dataclasses import dataclass

from app.models.mechanism import Mechanism


@dataclass
class MechanismValidationIssue:
    level: str
    code: str
    message: str
    entity_id: int


def validate_mechanisms_for_export(project) -> list[MechanismValidationIssue]:
    issues: list[MechanismValidationIssue] = []

    for mechanism in project.mechanisms:
        issues.extend(validate_mechanism(mechanism))

    return issues


def validate_mechanism(mechanism: Mechanism) -> list[MechanismValidationIssue]:
    issues: list[MechanismValidationIssue] = []

    if not str(mechanism.code or "").strip():
        issues.append(
            MechanismValidationIssue(
                level="error",
                code="missing_mechanism_code",
                message="Mechanism code is missing",
                entity_id=mechanism.id,
            )
        )

    if not str(mechanism.name or "").strip():
        issues.append(
            MechanismValidationIssue(
                level="error",
                code="missing_mechanism_name",
                message="Mechanism name is missing",
                entity_id=mechanism.id,
            )
        )

    if not str(mechanism.mechanism_type or "").strip():
        issues.append(
            MechanismValidationIssue(
                level="error",
                code="missing_mechanism_type",
                message="Mechanism type is missing",
                entity_id=mechanism.id,
            )
        )

    if mechanism.quantity is None or mechanism.quantity <= 0:
        issues.append(
            MechanismValidationIssue(
                level="error",
                code="invalid_quantity",
                message="Mechanism quantity must be greater than zero",
                entity_id=mechanism.id,
            )
        )

    if not str(mechanism.device_type or "").strip():
        issues.append(
            MechanismValidationIssue(
                level="error",
                code="missing_device_type",
                message="Device type is missing",
                entity_id=mechanism.id,
            )
        )

    if not str(mechanism.device_address or "").strip():
        issues.append(
            MechanismValidationIssue(
                level="error",
                code="missing_device_address",
                message="Device address is missing",
                entity_id=mechanism.id,
            )
        )

    if not str(mechanism.device_channel or "").strip():
        issues.append(
            MechanismValidationIssue(
                level="error",
                code="missing_device_channel",
                message="Device channel is missing",
                entity_id=mechanism.id,
            )
        )

    return issues

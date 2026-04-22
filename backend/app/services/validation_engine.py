from collections import Counter

from app.models.project import Project
from app.schemas.validation import ProjectValidationResult, ValidationIssue
from app.services.ets_generator import build_lighting_group_ets_preview


def validate_project_export(project: Project) -> ProjectValidationResult:
    issues: list[ValidationIssue] = []

    if not project.lighting_groups:
        issues.append(
            ValidationIssue(
                level="error",
                code="NO_LIGHTING_GROUPS",
                message="В проекте нет групп света для экспорта",
            )
        )

    all_rows = []
    for group in project.lighting_groups:
        preview = build_lighting_group_ets_preview(group)
        all_rows.extend(preview.rows)

    address_counts = Counter(row.group_address for row in all_rows)
    duplicate_addresses = [addr for addr, count in address_counts.items() if count > 1]
    for addr in duplicate_addresses:
        issues.append(
            ValidationIssue(
                level="error",
                code="DUPLICATE_GROUP_ADDRESS",
                message=f"Повторяется групповой адрес: {addr}",
            )
        )

    name_counts = Counter(row.name for row in all_rows)
    duplicate_names = [name for name, count in name_counts.items() if count > 1]
    for name in duplicate_names:
        issues.append(
            ValidationIssue(
                level="warning",
                code="DUPLICATE_NAME",
                message=f"Повторяется имя объекта: {name}",
            )
        )

    is_valid = not any(issue.level == "error" for issue in issues)

    return ProjectValidationResult(
        project_id=project.id,
        is_valid=is_valid,
        issues=issues,
    )

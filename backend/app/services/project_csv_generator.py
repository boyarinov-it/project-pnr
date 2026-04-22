import csv
import io

from app.core.standard_profile import STANDARD_PROFILE
from app.models.project import Project
from app.schemas.project_csv_preview import ProjectCsvPreview
from app.services.ets_generator import build_lighting_group_ets_preview


def build_project_lighting_csv_preview(project: Project) -> ProjectCsvPreview:
    columns = STANDARD_PROFILE["export"]["csv_columns"]
    separator = STANDARD_PROFILE["export"]["separator"]

    output = io.StringIO()
    writer = csv.writer(output, delimiter=separator)
    writer.writerow(columns)

    for group in project.lighting_groups:
        ets_preview = build_lighting_group_ets_preview(group)
        for row in ets_preview.rows:
            writer.writerow([getattr(row, column) for column in columns])

    filename = f"project_{project.id}_lighting.csv"

    return ProjectCsvPreview(
        project_id=project.id,
        project_name=project.name,
        filename=filename,
        content=output.getvalue(),
    )

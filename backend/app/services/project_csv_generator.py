import csv
import io

from app.models.project import Project
from app.schemas.project_csv_preview import ProjectCsvPreview
from app.services.ets_generator import build_lighting_group_ets_preview


def build_project_lighting_csv_preview(project: Project) -> ProjectCsvPreview:
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["group_address", "name", "datapoint_type", "function"])

    for group in project.lighting_groups:
        ets_preview = build_lighting_group_ets_preview(group)
        for row in ets_preview.rows:
            writer.writerow([
                row.group_address,
                row.name,
                row.datapoint_type,
                row.function,
            ])

    filename = f"project_{project.id}_lighting.csv"

    return ProjectCsvPreview(
        project_id=project.id,
        project_name=project.name,
        filename=filename,
        content=output.getvalue(),
    )

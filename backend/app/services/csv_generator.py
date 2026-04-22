import csv
import io

from app.models.lighting_group import LightingGroup
from app.schemas.csv_preview import LightingGroupCsvPreview
from app.services.ets_generator import build_lighting_group_ets_preview


def build_lighting_group_csv_preview(group: LightingGroup) -> LightingGroupCsvPreview:
    ets_preview = build_lighting_group_ets_preview(group)

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["group_address", "name", "datapoint_type", "function"])

    for row in ets_preview.rows:
        writer.writerow([
            row.group_address,
            row.name,
            row.datapoint_type,
            row.function,
        ])

    filename = f"lighting_group_{group.id}.csv"

    return LightingGroupCsvPreview(
        lighting_group_id=group.id,
        lighting_group_name=group.name,
        filename=filename,
        content=output.getvalue(),
    )

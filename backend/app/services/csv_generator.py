import csv
import io

from app.core.standard_profile import STANDARD_PROFILE
from app.models.lighting_group import LightingGroup
from app.schemas.csv_preview import LightingGroupCsvPreview
from app.services.ets_generator import build_lighting_group_ets_preview


def build_lighting_group_csv_preview(group: LightingGroup) -> LightingGroupCsvPreview:
    ets_preview = build_lighting_group_ets_preview(group)
    columns = STANDARD_PROFILE["export"]["csv_columns"]
    separator = STANDARD_PROFILE["export"]["separator"]

    output = io.StringIO()
    writer = csv.writer(output, delimiter=separator)
    writer.writerow(columns)

    for row in ets_preview.rows:
        writer.writerow([getattr(row, column) for column in columns])

    filename = f"lighting_group_{group.id}.csv"

    return LightingGroupCsvPreview(
        lighting_group_id=group.id,
        lighting_group_name=group.name,
        filename=filename,
        content=output.getvalue(),
    )

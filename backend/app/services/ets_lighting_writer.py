from app.rules.lighting_profile import LIGHTING_ETS_PROFILE
from app.services.description_builder import build_lighting_description
from app.services.ets_lighting_addressing import get_numbers_of_groups
from app.services.lighting_validator import validate_lighting_groups_for_export
from app.services.naming_builder import build_lighting_object_name

SOFT_LIGHTING_EXPORT_ERROR_CODES = {
    "missing_device_type",
    "missing_device_address",
    "missing_device_output",
    "missing_device_channel",
    "missing_dimmer_channel",
}


def filter_blocking_lighting_export_errors(error_text: str) -> str:
    errors = [
        item.strip()
        for item in str(error_text or "").replace(",", ";").split(";")
        if item.strip()
    ]

    blocking_errors = []

    for error in errors:
        code = error.split(":", 1)[0].strip()

        if code in SOFT_LIGHTING_EXPORT_ERROR_CODES:
            continue

        blocking_errors.append(error)

    return "; ".join(blocking_errors)



def is_rgbw_lighting_group(group: object) -> bool:
    return str(getattr(group, "load_type", "") or "").strip().upper() == "RGBW"



def build_lighting_ets_csv(project) -> str:
    issues = validate_lighting_groups_for_export(project)
    critical_errors = [x for x in issues if x.level == "error"]
    if critical_errors:
        error_text = "; ".join([f"{x.code}:{x.entity_id}" for x in critical_errors])
        blocking_error_text = filter_blocking_lighting_export_errors(error_text)
        if blocking_error_text:
            raise ValueError(f"Lighting export validation failed: {blocking_error_text}")

    rows: list[str] = []
    rows.extend(LIGHTING_ETS_PROFILE["header_rows"])

    for group in project.lighting_groups:

        if is_rgbw_lighting_group(group):

            continue
        number_of_current_group = int(group.code)
        full_group_number = get_numbers_of_groups(number_of_current_group)
        arr_group_numbers = full_group_number.split("/")
        group_counter2 = int(arr_group_numbers[1])
        group_counter3 = int(arr_group_numbers[2]) - 1

        for item in LIGHTING_ETS_PROFILE["function_rows"]:
            group_counter3 += 1

            object_name = build_lighting_object_name(group, item["label"])
            description = build_lighting_description(group)

            row = (
                f" , ,{object_name},"
                f"{LIGHTING_ETS_PROFILE['main_group']}/{group_counter2}/{group_counter3}"
                f",,,{description},{item['dpt']},Auto"
            )
            rows.append(row)

    return "\r\n".join(rows) + "\r\n"

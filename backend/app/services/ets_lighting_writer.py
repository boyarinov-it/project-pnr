from app.rules.lighting_profile import LIGHTING_ETS_PROFILE
from app.services.description_builder import build_lighting_description
from app.services.ets_lighting_addressing import get_numbers_of_groups
from app.services.lighting_validator import validate_lighting_groups_for_export


def build_lighting_ets_csv(project) -> str:
    issues = validate_lighting_groups_for_export(project)
    critical_errors = [x for x in issues if x.level == "error"]
    if critical_errors:
        error_text = "; ".join([f"{x.code}:{x.entity_id}" for x in critical_errors])
        raise ValueError(f"Lighting export validation failed: {error_text}")

    rows: list[str] = []
    rows.extend(LIGHTING_ETS_PROFILE["header_rows"])

    for group in project.lighting_groups:
        number_of_current_group = int(group.code)
        full_group_number = get_numbers_of_groups(number_of_current_group)
        arr_group_numbers = full_group_number.split("/")
        group_counter2 = int(arr_group_numbers[1])
        group_counter3 = int(arr_group_numbers[2]) - 1

        for item in LIGHTING_ETS_PROFILE["function_rows"]:
            group_counter3 += 1

            object_name = LIGHTING_ETS_PROFILE["naming"]["object_name_pattern"].format(
                group_code=group.code,
                function_label=item["label"],
                room_code=group.room.code,
                group_name=group.name,
            )

            description = build_lighting_description(group)

            row = (
                f" , ,{object_name},"
                f"{LIGHTING_ETS_PROFILE['main_group']}/{group_counter2}/{group_counter3}"
                f",,,{description},{item['dpt']},Auto"
            )
            rows.append(row)

    return "\r\n".join(rows) + "\r\n"

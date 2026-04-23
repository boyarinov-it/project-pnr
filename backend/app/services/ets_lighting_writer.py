from app.models.project import Project
from app.rules.lighting_profile import LIGHTING_ETS_PROFILE
from app.services.ets_lighting_addressing import get_numbers_of_groups


def build_lighting_ets_csv(project: Project) -> str:
    rows: list[str] = []
    rows.extend(LIGHTING_ETS_PROFILE["header_rows"])

    for group in project.lighting_groups:
        if not group.room:
            continue

        if not group.code or not str(group.code).isdigit():
            continue

        number_of_current_group = int(group.code)
        full_group_number = get_numbers_of_groups(number_of_current_group)
        arr_group_numbers = full_group_number.split("/")
        group_counter2 = int(arr_group_numbers[1])
        group_counter3 = int(arr_group_numbers[2]) - 1

        output_dimmer = ""
        if group.dimmer_channel:
            output_dimmer = f" - Диммер: {group.dimmer_channel}"

        for item in LIGHTING_ETS_PROFILE["function_rows"]:
            group_counter3 += 1

            object_name = (
                f"_{group.code}__{item['suffix']}_"
                f"{group.room.code}-{group.name}"
            )

            description = (
                f"{group.device_type or ''} "
                f"{group.device_address or ''} "
                f"Выход:{group.device_output or ''}"
                f"{output_dimmer} "
                f"Нагрузка:{group.load_type}"
            ).strip()

            row = (
                f" , ,{object_name},"
                f"{LIGHTING_ETS_PROFILE['main_group']}/{group_counter2}/{group_counter3},"
                f",,,{description},{item['dpt']},Auto"
            )
            rows.append(row)

    return "\r\n".join(rows) + "\r\n"

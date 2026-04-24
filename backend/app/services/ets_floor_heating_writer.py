from app.models.floor_heating import FloorHeating
from app.models.room import Room
from app.rules.floor_heating_profile import FLOOR_HEATING_ETS_PROFILE


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_floor_heating_description(item: FloorHeating) -> str:
    parts = []

    if item.device_type:
        parts.append(item.device_type)

    if item.device_address:
        parts.append(item.device_address)

    if item.device_channel:
        parts.append(f"Канал:{item.device_channel}")

    if item.thermostat_type:
        parts.append(f"Тип:{item.thermostat_type}")

    return " ".join(parts)


def get_floor_heating_group_address(index: int, offset: int) -> str:
    # 24 зон теплого пола в одной средней группе:
    # 3/1/10-19, 3/1/20-29 ... 3/1/240-249
    middle_group = index // 24 + 1
    third_group_base = 10 + (index % 24) * 10

    return f"{FLOOR_HEATING_ETS_PROFILE['main_group']}/{middle_group}/{third_group_base + offset}"


def build_floor_heating_object_name(item: FloorHeating, function_label: str) -> str:
    room = item.room
    room_name = build_room_name(room)

    return (
        f"_{item.code}_"
        f"{room.room_number}.{room_name} -{item.name}_"
        f"{function_label}"
    )


def build_floor_heating_ets_csv(project) -> str:
    rows: list[str] = []

    rows.append(f"{FLOOR_HEATING_ETS_PROFILE['main_group_name']}, , ,3/-/-,,,,,Auto")
    rows.append(f",{FLOOR_HEATING_ETS_PROFILE['group_name']}, ,3/1/-,,,,,Auto")

    for reserved in FLOOR_HEATING_ETS_PROFILE["reserved_rows"]:
        dpt = reserved["dpt"]
        rows.append(f" , ,{reserved['name']},{reserved['address']},,,,{dpt},Auto")

    floor_heating_items = sorted(project.floor_heating, key=lambda x: x.id)

    for index, item in enumerate(floor_heating_items):
        description = build_floor_heating_description(item)

        for function in FLOOR_HEATING_ETS_PROFILE["functions"]:
            address = get_floor_heating_group_address(index, function["offset"])
            object_name = build_floor_heating_object_name(item, function["label"])
            dpt = function["dpt"]

            if function["label"] == "Резерв":
                rows.append(f" , ,Резерв,{address},,,,,Auto")
            else:
                rows.append(f" , ,{object_name},{address},,,{description},{dpt},Auto")

    return "\r\n".join(rows) + "\r\n"

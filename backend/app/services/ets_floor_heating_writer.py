from app.models.floor_heating import FloorHeating
from app.models.room import Room
from app.rules.floor_heating_profile import FLOOR_HEATING_ETS_PROFILE


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_floor_heating_description(item: FloorHeating) -> str:
    parts = []

    if item.device_address or item.device_channel:
        output = str(item.device_address or "").strip()
        channel = str(item.device_channel or "").strip()

        if output and channel:
            parts.append(f"Выход: {output}/{channel}")
        elif output:
            parts.append(f"Выход: {output}")
        elif channel:
            parts.append(f"Выход: {channel}")

    if item.device_type:
        parts.append(f"Устройство: {item.device_type}")

    return " ".join(parts)


def build_floor_heating_reserved_description(item: FloorHeating) -> str:
    output = str(item.device_address or "").strip()
    channel = str(item.device_channel or "").strip()
    device = str(item.device_type or "").strip()

    if output and channel and device:
        return f"{output} {channel} Термостат:{device}"

    return build_floor_heating_description(item)


def get_floor_heating_group_address(index: int, offset: int) -> str:
    items_per_middle_group = FLOOR_HEATING_ETS_PROFILE["items_per_middle_group"]

    middle_group = index // items_per_middle_group + 1
    third_group_base = 10 + (index % items_per_middle_group) * 10

    return f"{FLOOR_HEATING_ETS_PROFILE['main_group']}/{middle_group}/{third_group_base + offset}"


def build_floor_heating_object_name(item: FloorHeating, function_label: str) -> str:
    room = item.room
    room_name = build_room_name(room)

    return f"_{item.code}_{room.room_number}.{room_name} __{function_label}"


def build_floor_heating_ets_csv(project) -> str:
    rows: list[str] = []

    rows.append(f"{FLOOR_HEATING_ETS_PROFILE['main_group_name']},,,{FLOOR_HEATING_ETS_PROFILE['main_group']}/-/-,,,,,Auto")
    rows.append(f",{FLOOR_HEATING_ETS_PROFILE['group_name']}, ,{FLOOR_HEATING_ETS_PROFILE['main_group']}/1/-,,,,,Auto")

    for reserved in FLOOR_HEATING_ETS_PROFILE["reserved_rows"]:
        rows.append(f", ,{reserved['name']},{reserved['address']},,,,{reserved['dpt']},Auto")

    floor_heating_items = sorted(project.floor_heating, key=lambda x: x.id)

    for index, item in enumerate(floor_heating_items):
        description = build_floor_heating_description(item)
        reserved_description = build_floor_heating_reserved_description(item)

        for function in FLOOR_HEATING_ETS_PROFILE["functions"]:
            address = get_floor_heating_group_address(index, function["offset"])
            dpt = function["dpt"]

            if function.get("reserved"):
                rows.append(f" , ,Резерв,{address},,,{reserved_description},{dpt},Auto")
            else:
                object_name = build_floor_heating_object_name(item, function["label"])
                rows.append(f" , ,{object_name},{address},,,{description},{dpt},Auto")

    return "\r\n".join(rows) + "\r\n"

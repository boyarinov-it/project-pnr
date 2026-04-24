from app.models.fan import Fan
from app.models.room import Room
from app.rules.fans_profile import FANS_ETS_PROFILE


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_fan_description(fan: Fan) -> str:
    parts = []

    if fan.device_type:
        parts.append(fan.device_type)

    if fan.device_address:
        parts.append(fan.device_address)

    if fan.device_channel:
        parts.append(f"Канал:{fan.device_channel}")

    return " ".join(parts)


def get_fan_group_address(index: int, offset: int) -> str:
    items_per_middle_group = FANS_ETS_PROFILE["items_per_middle_group"]

    middle_group = index // items_per_middle_group + 1
    third_group_base = (
        FANS_ETS_PROFILE["start_address"]
        + (index % items_per_middle_group) * FANS_ETS_PROFILE["addresses_per_fan"]
    )

    return f"{FANS_ETS_PROFILE['main_group']}/{middle_group}/{third_group_base + offset}"


def build_fan_object_name(fan: Fan, function_label: str) -> str:
    room = fan.room
    room_name = build_room_name(room)

    return f"_{fan.code}_{room.room_number}.{room_name} -{fan.name}_{function_label}"


def build_fans_ets_csv(project) -> str:
    rows: list[str] = []

    rows.append(f"{FANS_ETS_PROFILE['main_group_name']},,,8/-/-,,,,,Auto")
    rows.append(f",{FANS_ETS_PROFILE['group_name']}, ,8/1/-,,,,,Auto")

    for reserved in FANS_ETS_PROFILE["reserved_rows"]:
        dpt = reserved["dpt"]
        rows.append(f",,{reserved['name']},{reserved['address']},,,,{dpt},Auto")

    fans = sorted(project.fans, key=lambda x: x.id)

    for index, fan in enumerate(fans):
        description = build_fan_description(fan)

        for function in FANS_ETS_PROFILE["functions"]:
            address = get_fan_group_address(index, function["offset"])
            object_name = build_fan_object_name(fan, function["label"])
            dpt = function["dpt"]

            rows.append(f",,{object_name},{address},,,{description},{dpt},Auto")

    return "\r\n".join(rows) + "\r\n"

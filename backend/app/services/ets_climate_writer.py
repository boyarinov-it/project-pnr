from app.models.climate import Climate
from app.models.room import Room
from app.rules.climate_profile import CLIMATE_ETS_PROFILE


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_climate_description(item: Climate) -> str:
    parts = []

    if item.device_address or item.device_channel:
        output = str(item.device_address or "").strip()
        channel = str(item.device_channel or "").strip()

        if output and channel:
            parts.append(f"Выход {output}/{channel}")
        elif output:
            parts.append(f"Выход {output}")
        elif channel:
            parts.append(f"Выход {channel}")

    if item.device_type:
        parts.append(f"Устройство:{item.device_type}")

    if item.gateway_address:
        parts.append(f"Шлюз:{item.gateway_address}")

    if item.external_id:
        parts.append(f"ID:{item.external_id}")

    return " ".join(parts)


def get_climate_group_address(index: int, offset: int) -> str:
    items_per_middle_group = CLIMATE_ETS_PROFILE["items_per_middle_group"]

    middle_group = index // items_per_middle_group + 1
    third_group_base = 10 + (index % items_per_middle_group) * 20

    return f"{CLIMATE_ETS_PROFILE['main_group']}/{middle_group}/{third_group_base + offset}"


def build_climate_object_name(item: Climate, function_label: str) -> str:
    room = item.room
    room_name = build_room_name(room)

    return f"_{item.code}_{room.room_number}.{room_name} __{function_label}"


def build_climate_ets_csv(project) -> str:
    rows: list[str] = []

    rows.append(f"{CLIMATE_ETS_PROFILE['main_group_name']},,,{CLIMATE_ETS_PROFILE['main_group']}/-/-,,,,,Auto")
    rows.append(f",{CLIMATE_ETS_PROFILE['group_name']}, ,{CLIMATE_ETS_PROFILE['main_group']}/1/-,,,,,Auto")

    for reserved in CLIMATE_ETS_PROFILE["reserved_rows"]:
        rows.append(f",,{reserved['name']},{reserved['address']},,,,{reserved['dpt']},Auto")

    climate_items = sorted(project.climate, key=lambda x: x.id)

    for index, item in enumerate(climate_items):
        description = build_climate_description(item)

        for function in CLIMATE_ETS_PROFILE["functions"]:
            address = get_climate_group_address(index, function["offset"])
            object_name = build_climate_object_name(item, function["label"])
            dpt = function["dpt"]

            rows.append(f",,{object_name},{address},,,{description},{dpt},Auto")

    return "\r\n".join(rows) + "\r\n"

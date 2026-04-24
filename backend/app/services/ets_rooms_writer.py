from app.models.room import Room
from app.rules.rooms_profile import ROOMS_ETS_PROFILE


def build_room_export_name(room: Room) -> str:
    room_number = str(room.room_number or "").strip()
    room_name = room.name_ru or room.name or room.code

    return f"{room_number}_{room_name}"


def get_room_sort_key(room: Room):
    room_number = str(room.room_number or "").strip()

    if room_number.isdigit():
        return (0, int(room_number))

    return (1, room_number)


def get_room_group_address(index: int, offset: int) -> str:
    base = ROOMS_ETS_PROFILE["start_address"] + index * ROOMS_ETS_PROFILE["addresses_per_room"]

    return (
        f"{ROOMS_ETS_PROFILE['main_group']}/"
        f"{ROOMS_ETS_PROFILE['middle_group']}/"
        f"{base + offset}"
    )


def build_room_object_name(room: Room, function_label: str) -> str:
    return f"{build_room_export_name(room)}_{function_label}"


def build_rooms_ets_csv(project) -> str:
    rows: list[str] = []

    rows.append(
        f"{ROOMS_ETS_PROFILE['main_group_name']},,,"
        f"{ROOMS_ETS_PROFILE['main_group']}/-/-,,,,,Auto"
    )
    rows.append(
        f",{ROOMS_ETS_PROFILE['middle_group_name']}, ,"
        f"{ROOMS_ETS_PROFILE['main_group']}/{ROOMS_ETS_PROFILE['middle_group']}/-,,,,,Auto"
    )

    rooms = sorted(project.rooms, key=get_room_sort_key)

    for index, room in enumerate(rooms):
        for function in ROOMS_ETS_PROFILE["functions"]:
            address = get_room_group_address(index, function["offset"])
            object_name = build_room_object_name(room, function["label"])
            dpt = function["dpt"]

            rows.append(f",,{object_name},{address},,,,{dpt},Auto")

    return "\r\n".join(rows) + "\r\n"

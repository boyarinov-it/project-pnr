from app.models.mechanism import Mechanism
from app.models.room import Room
from app.rules.mechanisms_profile import MECHANISMS_ETS_PROFILE


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_mechanism_description(mechanism: Mechanism) -> str:
    parts = []

    if mechanism.device_type:
        parts.append(mechanism.device_type)

    if mechanism.device_address:
        parts.append(mechanism.device_address)

    if mechanism.device_channel:
        parts.append(f"Канал:{mechanism.device_channel}")

    if mechanism.mechanism_type:
        parts.append(f"Механизм:{mechanism.mechanism_type}")

    return " ".join(parts)


def get_mechanism_group_address(index: int, offset: int) -> str:
    # 24 механизма в одной средней группе:
    # 2/1/10-19, 2/1/20-29 ... 2/1/240-249
    block_index = index
    middle_group = block_index // 24 + 1
    third_group_base = 10 + (block_index % 24) * 10

    return f"{MECHANISMS_ETS_PROFILE['main_group']}/{middle_group}/{third_group_base + offset}"


def build_mechanism_object_name(mechanism: Mechanism, function_label: str) -> str:
    room = mechanism.room
    room_name = build_room_name(room)

    return (
        f"_{mechanism.code}_"
        f"{room.room_number}.{room_name} -{mechanism.name}_"
        f"{function_label}"
    )


def build_mechanisms_ets_csv(project) -> str:
    rows: list[str] = []

    rows.append(f"{MECHANISMS_ETS_PROFILE['main_group_name']}, , ,2/-/-,,,,,Auto")
    rows.append(f",{MECHANISMS_ETS_PROFILE['group_name']}, ,2/1/-,,,,,Auto")

    for reserved in MECHANISMS_ETS_PROFILE["reserved_rows"]:
        dpt = reserved["dpt"]
        rows.append(f" , ,{reserved['name']},{reserved['address']},,,,{dpt},Auto")

    mechanisms = sorted(project.mechanisms, key=lambda x: x.id)

    for index, mechanism in enumerate(mechanisms):
        description = build_mechanism_description(mechanism)

        for function in MECHANISMS_ETS_PROFILE["functions"]:
            address = get_mechanism_group_address(index, function["offset"])
            object_name = build_mechanism_object_name(mechanism, function["label"])
            dpt = function["dpt"]

            if function["label"] == "Резерв":
                rows.append(f" , ,Резерв,{address},,,,,Auto")
            else:
                rows.append(f" , ,{object_name},{address},,,,{description},{dpt},Auto")

    return "\r\n".join(rows) + "\r\n"

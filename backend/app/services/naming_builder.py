from app.rules.lighting_profile import LIGHTING_ETS_PROFILE


def build_lighting_object_name(group, function_label: str) -> str:
    locale = LIGHTING_ETS_PROFILE["naming"]["locale"]

    room_name_ru = group.room.name_ru or group.room.name or group.room.code
    room_name_en = group.room.name_en or group.room.name or group.room.code

    if locale == "ru":
        pattern = LIGHTING_ETS_PROFILE["naming"]["object_name_pattern_ru"]
        return pattern.format(
            group_code=group.code,
            function_label=function_label,
            room_name_ru=room_name_ru,
            group_name=group.name,
        )

    if locale == "en":
        pattern = LIGHTING_ETS_PROFILE["naming"]["object_name_pattern_en"]
        return pattern.format(
            group_code=group.code,
            function_label=function_label,
            room_name_en=room_name_en,
            group_name=group.name,
        )

    pattern = LIGHTING_ETS_PROFILE["naming"]["object_name_pattern_code"]
    return pattern.format(
        group_code=group.code,
        function_label=function_label,
        room_code=group.room.code,
        group_name=group.name,
    )

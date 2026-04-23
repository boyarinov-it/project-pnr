from app.rules.lighting_profile import LIGHTING_ETS_PROFILE


def get_numbers_of_groups(number_of_current_group: int) -> str:
    main_number_of_group = LIGHTING_ETS_PROFILE["main_group"]
    number_of_blocks_in_group = LIGHTING_ETS_PROFILE["blocks_in_middle_group"]
    number_of_rows_in_block = LIGHTING_ETS_PROFILE["rows_in_block"]

    bl_is_integer = (number_of_current_group % number_of_blocks_in_group) == 0
    x = number_of_current_group // number_of_blocks_in_group
    y = x if bl_is_integer else x + 1
    z = number_of_current_group - x * number_of_blocks_in_group
    third_group = (
        number_of_rows_in_block * number_of_blocks_in_group
        if bl_is_integer
        else z * number_of_rows_in_block
    )
    return f"{main_number_of_group}/{y}/{third_group}"

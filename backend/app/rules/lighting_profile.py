from app.core.standard_profile import STANDARD_PROFILE

LIGHTING_ETS_PROFILE = {
    "main_group": STANDARD_PROFILE["main_groups"][STANDARD_PROFILE["lighting"]["main_group_key"]],
    "blocks_in_middle_group": STANDARD_PROFILE["lighting"]["grouping"]["blocks_in_middle_group"],
    "rows_in_block": STANDARD_PROFILE["lighting"]["grouping"]["rows_in_block"],
    "start_index_group3": STANDARD_PROFILE["lighting"]["grouping"]["start_index_group3"],
    "header_rows": STANDARD_PROFILE["lighting"]["header_rows"],
    "function_rows": STANDARD_PROFILE["lighting"]["functions"],
    "validation": STANDARD_PROFILE["lighting"]["validation"],
    "description": STANDARD_PROFILE["lighting"]["description"],
    "naming": STANDARD_PROFILE["lighting"]["naming"],
}

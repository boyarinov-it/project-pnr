from app.core.standard_profile import STANDARD_PROFILE


LIGHTING_ETS_PROFILE = {
    "main_group": STANDARD_PROFILE["main_groups"]["lighting"],
    "start_index_group3": STANDARD_PROFILE["lighting"]["middle_group"]["start_index_group3"],
    "blocks_in_middle_group": STANDARD_PROFILE["lighting"]["middle_group"]["blocks_in_middle_group"],
    "rows_in_block": STANDARD_PROFILE["lighting"]["middle_group"]["rows_in_block"],
    "csv_separator": STANDARD_PROFILE["export"]["separator"],
    "header_rows": STANDARD_PROFILE["lighting"]["header_rows"],
    "function_rows": STANDARD_PROFILE["lighting"]["functions"],
}

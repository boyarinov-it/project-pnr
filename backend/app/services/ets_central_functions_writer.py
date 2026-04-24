from app.rules.central_functions_profile import CENTRAL_FUNCTIONS_ETS_PROFILE


def build_central_functions_ets_csv() -> str:
    rows: list[str] = []

    rows.append(
        f"{CENTRAL_FUNCTIONS_ETS_PROFILE['main_group_name']},,,"
        f"{CENTRAL_FUNCTIONS_ETS_PROFILE['main_group']}/-/-,,,,,Auto"
    )

    rows.append(
        f",{CENTRAL_FUNCTIONS_ETS_PROFILE['middle_group_name']}, ,"
        f"{CENTRAL_FUNCTIONS_ETS_PROFILE['main_group']}/"
        f"{CENTRAL_FUNCTIONS_ETS_PROFILE['middle_group']}/-,,,,,Auto"
    )

    for function in CENTRAL_FUNCTIONS_ETS_PROFILE["functions"]:
        rows.append(
            f",,{function['name']},{function['address']},,,"
            f"{function['description']},{function['dpt']},Auto"
        )

    return "\r\n".join(rows) + "\r\n"

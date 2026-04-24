FANS_ETS_PROFILE = {
    "main_group": 8,
    "main_group_name": "Вытяжные вентиляторы",
    "group_name": "1-125",
    "items_per_middle_group": 125,
    "start_address": 5,
    "addresses_per_fan": 2,
    "reserved_rows": [
        {"address": "8/1/0", "name": "Все Вент", "dpt": "DPST-1-1"},
        {"address": "8/1/1", "name": "Резерв", "dpt": ""},
        {"address": "8/1/2", "name": "Резерв", "dpt": ""},
        {"address": "8/1/3", "name": "Резерв", "dpt": ""},
        {"address": "8/1/4", "name": "Резерв", "dpt": ""},
    ],
    "functions": [
        {"offset": 0, "label": "Вкл", "dpt": "DPST-1-1"},
        {"offset": 1, "label": "Статус", "dpt": "DPST-1-1"},
    ],
}

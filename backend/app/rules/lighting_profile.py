LIGHTING_ETS_PROFILE = {
    "main_group": 1,
    "start_index_group3": 5,
    "blocks_in_middle_group": 50,
    "rows_in_block": 5,
    "csv_separator": ",",
    "header_rows": [
        "Освещение, , ,1/-/-,,,,,Auto",
        ",1-50, ,1/1/-,,,,,Auto",
        ", ,Выключение всего освещения,1/1/0,,,,DPST-1-1,Auto",
        ", ,Мастер резерв,1/1/1,,,,,Auto",
        ", ,Мастер резерв,1/1/2,,,,,Auto",
        ", ,Мастер резерв,1/1/3,,,,,Auto",
        ", ,Мастер резерв,1/1/4,,,,,Auto",
    ],
    "function_rows": [
        {"index": 1, "suffix": "Вкл", "dpt": "DPST-1-1"},
        {"index": 2, "suffix": "Димм", "dpt": "DPST-3-7"},
        {"index": 3, "suffix": "Яркость%", "dpt": "DPST-5-1"},
        {"index": 4, "suffix": "Статус", "dpt": "DPST-1-1"},
        {"index": 5, "suffix": "Статус%", "dpt": "DPST-5-1"},
    ],
}


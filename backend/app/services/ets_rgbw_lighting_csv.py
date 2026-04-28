from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.lighting_group import LightingGroup
from app.models.room import Room
# SQLAlchemy model registry imports.
# Нужны, чтобы string relationships в Project корректно разрешались при отдельном запуске RGBW exporter.
from app.models.mechanism import Mechanism  # noqa: F401
from app.models.floor_heating import FloorHeating  # noqa: F401
from app.models.climate import Climate  # noqa: F401

try:
    from app.models.fans import Fan  # noqa: F401
except Exception:
    try:
        from app.models.fan import Fan  # noqa: F401
    except Exception:
        pass

from app.models.mechanism import Mechanism  # noqa: F401


@dataclass(frozen=True)
class RgbwCsvRow:
    name: str
    address: str
    description: str
    datapoint: str | None


RGBW_FUNCTIONS = [
    ("Вкл/выкл", "DPST-1-1"),
    ("Димм", "DPST-3-7"),
    ("Яркость%", "DPST-5-1"),
    ("Статус", "DPST-1-1"),
    ("Статус%", "DPST-5-1"),
    ("RGBW_Димм", "DPST-251-600"),
    ("Статус_RGBW_Димм", "DPST-251-600"),
    ("Резерв1", None),
    ("Резерв2", None),
    ("Резерв3", None),
]


def build_rgbw_lighting_ets_csv(db: Session, project_id: int) -> str:
    groups = (
        db.query(LightingGroup)
        .filter(LightingGroup.project_id == project_id)
        .order_by(LightingGroup.id.asc())
        .all()
    )

    rgbw_groups = [
        group for group in groups
        if safe_text(getattr(group, "load_type", "")).upper() == "RGBW"
    ]

    lines: list[str] = [
        "RGBW DALI2 DT8,,,21/-/-,,,,,Auto",
        " ,1-25, ,21/1/-,,,,,Auto",
    ]

    current_middle_group = 1

    for group in rgbw_groups:
        group_number = parse_rgbw_group_number(getattr(group, "code", None))
        middle_group = get_rgbw_middle_group(group_number)

        if middle_group != current_middle_group:
            start = (middle_group - 1) * 25 + 1
            end = middle_group * 25
            lines.append(f" ,{start}-{end}, ,21/{middle_group}/-,,,,,Auto")
            current_middle_group = middle_group

        room_number = safe_text(getattr(group, "room_number", ""))
        room = find_room(db, project_id, room_number)
        room_title = build_room_title(room_number, room)
        description = build_description(group)

        for row in build_rgbw_rows(group, group_number, room_title, description):
            datapoint = row.datapoint or ""
            lines.append(
                f" , ,{row.name},{row.address},,,{row.description},{datapoint},Auto"
            )

    return "\r\n".join(lines) + "\r\n"


def safe_text(value: object) -> str:
    if value is None:
        return ""

    return str(value).strip()


def parse_rgbw_group_number(code: str | int | None) -> int:
    value = safe_text(code).upper()
    match = re.search(r"\d+", value)

    if not match:
        raise ValueError(f"invalid_rgbw_group_code:{code}")

    number = int(match.group())

    if number <= 0:
        raise ValueError(f"invalid_rgbw_group_code:{code}")

    return number


def get_rgbw_middle_group(group_number: int) -> int:
    return ((group_number - 1) // 25) + 1


def get_rgbw_third_group_base(group_number: int) -> int:
    index_inside_middle_group = ((group_number - 1) % 25) + 1
    return index_inside_middle_group * 10


def find_room(db: Session, project_id: int, room_number: str) -> Room | None:
    if not room_number:
        return None

    return (
        db.query(Room)
        .filter(Room.project_id == project_id)
        .filter(Room.room_number == room_number)
        .first()
    )


def build_room_title(room_number: str, room: Room | None) -> str:
    room_name = ""

    if room:
        room_name = (
            safe_text(getattr(room, "name_ru", ""))
            or safe_text(getattr(room, "name", ""))
            or safe_text(getattr(room, "code", ""))
        )

    if room_number and room_name:
        return f"{room_number}.{room_name}"

    return room_number or room_name


def get_first_existing_attr(obj: object, names: list[str]) -> str:
    for name in names:
        value = safe_text(getattr(obj, name, ""))
        if value:
            return value

    return ""


def build_description(group: LightingGroup) -> str:
    parts: list[str] = []

    device_address = get_first_existing_attr(group, ["device_address", "address"])
    device_type = get_first_existing_attr(group, ["device_type", "device"])
    device_output = get_first_existing_attr(
        group,
        ["device_output", "device_channel", "channel", "output"],
    )

    device_part = f"{device_address} {device_type}".strip()

    if device_part:
        parts.append(device_part)

    if device_output:
        parts.append(f"Выход:{device_output}")

    parts.append("Нагрузка:RGBW")

    return " ".join(parts)


def build_rgbw_rows(
    group: LightingGroup,
    group_number: int,
    room_title: str,
    description: str,
) -> Iterable[RgbwCsvRow]:
    middle_group = get_rgbw_middle_group(group_number)
    third_group_base = get_rgbw_third_group_base(group_number)
    code_label = f"C{group_number}"
    group_name = safe_text(getattr(group, "name", ""))

    title = f"{room_title}-{group_name}".strip("-")

    for index, (function_name, datapoint) in enumerate(RGBW_FUNCTIONS):
        address = f"21/{middle_group}/{third_group_base + index}"

        if function_name.startswith("Резерв"):
            name = f"_{code_label}_{function_name}"
            row_description = ""
        else:
            name = f"_{code_label}_{function_name}_{title}"
            row_description = description

        yield RgbwCsvRow(
            name=name,
            address=address,
            description=row_description,
            datapoint=datapoint,
        )

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.room import Room
from app.models.socket_contactor import SocketContactor


@dataclass(frozen=True)
class SocketContactorCsvRow:
    name: str
    address: str
    description: str
    datapoint: str


def build_sockets_contactors_ets_csv(db: Session, project_id: int) -> str:
    items = (
        db.query(SocketContactor)
        .filter(SocketContactor.project_id == project_id)
        .order_by(SocketContactor.id.asc())
        .all()
    )

    sorted_items = sorted(items, key=lambda item: (parse_group_number(item.code), item.id))

    lines: list[str] = [
        "Розетки и контакторы,,,7/-/-,,,,,Auto",
        " ,1-125, ,7/1/-,,,,,Auto",
        " , ,Выкл ВСЕ нагрузки,7/1/0,,,,DPST-1-1,Auto",
    ]

    current_middle_group = 1

    for item in sorted_items:
        group_number = parse_group_number(item.code)
        middle_group = get_middle_group(group_number)

        if middle_group != current_middle_group:
            start = (middle_group - 1) * 125 + 1
            end = middle_group * 125
            lines.append(f" ,{start}-{end}, ,7/{middle_group}/-,,,,,Auto")
            current_middle_group = middle_group

        room = find_room(db, project_id, item.room_number)
        room_title = build_room_title(item.room_number, room)
        description = build_description(item)

        for row in build_rows(item, group_number, room_title, description):
            lines.append(
                f" , ,{row.name},{row.address},,,{row.description},{row.datapoint},Auto"
            )

    return "\r\n".join(lines) + "\r\n"


def safe_text(value: object) -> str:
    if value is None:
        return ""

    return str(value).strip()


def parse_group_number(code: str | int | None) -> int:
    value = safe_text(code)
    match = re.search(r"\d+", value)

    if not match:
        raise ValueError(f"invalid_socket_contactor_code:{code}")

    number = int(match.group())

    if number <= 0:
        raise ValueError(f"invalid_socket_contactor_code:{code}")

    return number


def get_middle_group(group_number: int) -> int:
    return ((group_number - 1) // 125) + 1


def get_third_group_base(group_number: int) -> int:
    index_inside_middle_group = ((group_number - 1) % 125) + 1
    return (index_inside_middle_group - 1) * 2 + 1


def find_room(db: Session, project_id: int, room_number: str | None) -> Room | None:
    room_number = safe_text(room_number)

    if not room_number:
        return None

    return (
        db.query(Room)
        .filter(Room.project_id == project_id)
        .filter(Room.room_number == room_number)
        .first()
    )


def build_room_title(room_number: str | None, room: Room | None) -> str:
    room_number = safe_text(room_number)
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


def build_load_label(item: SocketContactor) -> str:
    load_type = safe_text(item.load_type).upper()

    labels = {
        "SOCKET": "Розетка",
        "CONTACTOR": "Контактор",
        "LIGHT": "Светильник",
    }

    return labels.get(load_type, safe_text(item.load_type) or "Нагрузка")


def build_description(item: SocketContactor) -> str:
    parts: list[str] = []

    device_address = safe_text(item.device_address)
    device_type = safe_text(item.device_type)
    device_output = safe_text(item.device_output)

    device_part = f"{device_address} {device_type}".strip()

    if device_part:
        parts.append(device_part)

    if device_output:
        parts.append(f"Выход:{device_output}")

    load_label = build_load_label(item)
    parts.append(f"Нагрузка:{load_label}")

    extra_description = safe_text(item.description)
    if extra_description:
        parts.append(extra_description)

    return " ".join(parts)


def build_rows(
    item: SocketContactor,
    group_number: int,
    room_title: str,
    description: str,
) -> Iterable[SocketContactorCsvRow]:
    middle_group = get_middle_group(group_number)
    third_group_base = get_third_group_base(group_number)

    code = safe_text(item.code)
    name = safe_text(item.name)
    load_label = build_load_label(item)

    title_parts = [room_title, name]
    title = "-".join([part for part in title_parts if part])

    if not title:
        title = load_label

    yield SocketContactorCsvRow(
        name=f"_{code}_Вкл_{title}",
        address=f"7/{middle_group}/{third_group_base}",
        description=description,
        datapoint="DPST-1-1",
    )

    yield SocketContactorCsvRow(
        name=f"_{code}_Статус_{title}",
        address=f"7/{middle_group}/{third_group_base + 1}",
        description=description,
        datapoint="DPST-1-1",
    )

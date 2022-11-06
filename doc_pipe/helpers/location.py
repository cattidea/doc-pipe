from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Location:
    lineno: int
    col_offset: int


@dataclass
class ReplacementInfo:
    start: Location
    end: Location
    replacement: str


def crop_string(text: str, start: Location, end: Location) -> str:
    lines_length = [len(line) + 1 for line in text.splitlines()]
    start_index = sum(lines_length[: start.lineno - 1]) + start.col_offset
    end_index = sum(lines_length[: end.lineno - 1]) + end.col_offset
    return text[start_index:end_index]


def replace_with_location(text: str, to_replace: list[ReplacementInfo]) -> str:
    lines_length = [len(line) + 1 for line in text.splitlines()]
    out = ""

    index = 0

    for to_replace_info in to_replace:
        start_index = sum(lines_length[: to_replace_info.start.lineno - 1]) + to_replace_info.start.col_offset
        end_index = sum(lines_length[: to_replace_info.end.lineno - 1]) + to_replace_info.end.col_offset
        out += text[index:start_index] + to_replace_info.replacement
        index = end_index

    out += text[index:]
    return out

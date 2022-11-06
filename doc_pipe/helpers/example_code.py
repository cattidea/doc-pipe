from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Iterable

from .docstring import Docstring
from .location import Location


@dataclass
class ExampleCode:
    code: str
    is_valid: bool
    offset: int
    start: Location
    end: Location


def _calc_offset(line: str) -> int:
    return len(line) - len(line.lstrip())


def _line_without_offset(line: str, offset: int) -> str:
    return line[offset:]


def _validate_code(code: str) -> bool:
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    return True


def extract_example_code(docstring: Docstring) -> Iterable[ExampleCode]:
    source = docstring.source
    lines = source.splitlines()
    start_idx, end_idx = docstring.start.lineno - 1, docstring.end.lineno - 1
    line_idx = start_idx
    while line_idx <= end_idx:
        line = lines[line_idx]

        # reStructureText
        # TODO: use regex
        if line.lstrip().startswith(".. code-block:: python"):
            example_code_min_offset = _calc_offset(line)

            # find the first line of the example code
            line_idx += 1
            while line_idx <= end_idx and (
                not lines[line_idx].lstrip()  # empty
                or lines[line_idx].lstrip().startswith(":")  # a directive attribute
            ):
                line_idx += 1

            example_code_first_line = lines[line_idx]
            example_code_offset = _calc_offset(example_code_first_line)
            if example_code_offset < example_code_min_offset:  # example code is empty
                continue

            # find other lines of the example code
            example = [_line_without_offset(example_code_first_line, example_code_offset)]
            example_code_start = Location(1, example_code_offset)
            line_idx += 1
            while line_idx <= end_idx and (not lines[line_idx] or _calc_offset(lines[line_idx]) >= example_code_offset):
                example.append(_line_without_offset(lines[line_idx], example_code_offset))
                line_idx += 1
            example_code = "\n".join(example)
            example_code_end = Location(line_idx + 1, len(lines[line_idx]))
            is_valid = _validate_code(example_code)
            yield ExampleCode(example_code, is_valid, example_code_offset, example_code_start, example_code_end)

        # Markdown
        if line.lstrip().startswith("``` python"):
            example_code_offset = _calc_offset(line)

            # find the first line of the example code
            line_idx += 1
            while line_idx <= end_idx and not lines[line_idx].lstrip():  # skip empty lines
                line_idx += 1

            example_code_first_line = lines[line_idx]

            # find other lines of the example code
            example = [_line_without_offset(example_code_first_line, example_code_offset)]
            example_code_start = Location(1, example_code_offset)
            line_idx += 1
            while (
                line_idx <= end_idx
                and (not lines[line_idx] or _calc_offset(lines[line_idx]) >= example_code_offset)
                and "```" not in lines[line_idx]
            ):
                example.append(_line_without_offset(lines[line_idx], example_code_offset))
                line_idx += 1

            if "```" in lines[line_idx]:
                example.append(_line_without_offset(lines[line_idx].removesuffix("```"), example_code_offset))
                example_code_end = Location(line_idx + 1, len(lines[line_idx]) - 3)
            else:
                example_code_end = Location(line_idx + 1, len(lines[line_idx]))
            example_code = "\n".join(example)
            is_valid = _validate_code(example_code)

            yield ExampleCode(example_code, is_valid, example_code_offset, example_code_start, example_code_end)

        # loop increment
        line_idx += 1

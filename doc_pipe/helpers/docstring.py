from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .location import Location, crop_string


class DocstringType(Enum):
    MODULE = "Module"
    CLASS = "Class"
    FUNCTION = "Function/Method"

    @staticmethod
    def from_node_type(node_type: type[ast.AST]) -> DocstringType:
        if node_type == ast.Module:
            return DocstringType.MODULE
        elif node_type == ast.ClassDef:
            return DocstringType.CLASS
        elif node_type == ast.FunctionDef:
            return DocstringType.FUNCTION
        else:
            raise ValueError(f"Unknown node type {node_type}")


@dataclass
class Docstring:
    type: DocstringType
    name: str
    source: str
    start: Location
    end: Location
    raw_value: str
    value: str


def extract_docstrings(source: str) -> Iterable[Docstring]:
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
            docstring_value = ast.get_docstring(node)
            docstring_type = DocstringType.from_node_type(type(node))
            docstring_name = node.name if not isinstance(node, ast.Module) else "<Mod>"
            if docstring_value is None:
                continue
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)  # docstring is the first statement
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                docstring_node = node.body[0].value
                start = Location(docstring_node.lineno, docstring_node.col_offset)
                end = Location(docstring_node.end_lineno, docstring_node.end_col_offset)  # type: ignore
                docstring_raw_value = crop_string(source, start, end)
                yield Docstring(
                    type=docstring_type,
                    name=docstring_name,
                    source=source,
                    start=start,
                    end=end,
                    raw_value=docstring_raw_value,
                    value=docstring_value,
                )

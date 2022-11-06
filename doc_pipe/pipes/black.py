from __future__ import annotations

import subprocess
from typing import Iterable

from typing_extensions import TypeAlias

from doc_pipe.helpers.example_code import ExampleCode
from doc_pipe.helpers.location import ReplacementInfo, Source
from doc_pipe.pipes.pipe import Pipe

ExampleCodeWithSource: TypeAlias = tuple[ExampleCode, Source]


class Black(Pipe):
    def __init__(self):
        super().__init__("Black")

    def match_args(self, args: list[str]) -> bool:
        return args[0] == "black"

    def run(self, args: list[str], examples: Iterable[ExampleCodeWithSource]) -> None:
        for example, _ in examples:
            example.write_to_cache()
        # TODO: non-blocking
        print([str(example.cache_path) for example, _ in examples])
        ret = subprocess.run(
            args + [str(example.cache_path) for example, _ in examples], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )  # pyright: reportUnusedVariable=false
        # TODO
        # stdout = ret.stdout.decode()
        # stderr = ret.stderr.decode()
        # retcode = ret.returncode

        for example, source in examples:
            example.update_from_cache()
            code_with_offset = example.get_code_with_offset()
            source.replace(ReplacementInfo(example.start, example.end, code_with_offset))

        # for _, source in examples:
        #     print(source.get_replaced_content())

        for _, source in examples:
            assert source.path is not None
            source.path.write_text(source.get_replaced_content(), encoding="utf-8")

    def process_output(self, output: str) -> str:
        ...

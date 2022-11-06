from __future__ import annotations

import argparse
import inspect
from pathlib import Path

from doc_pipe import __version__
from doc_pipe.cache import create_cache_dir
from doc_pipe.helpers.docstring import extract_docstrings
from doc_pipe.helpers.example_code import extract_example_code
from doc_pipe.helpers.location import Source
from doc_pipe.pipes import Black


def _get_source_from_string() -> Source:  # pyright: reportUnusedFunction=false
    code = """
    '''
    module docstirng
    '''

    def func():
        '''
        func docstring

        .. code-block:: python

            import os

            a = 1
            print(a)
        '''
        pass

    class Class:
        '''
        class docstring

        ``` python
        import os

        b =  2
        print(b)
        ```
        '''
        pass

    """
    code = inspect.cleandoc(code)
    return Source(content=code, path=None)


def _get_source_from_path() -> Source:
    path = Path("tests/file_test_0.py")
    return Source(content=path.read_text(encoding="utf-8"), path=path)


def test() -> None:

    source = _get_source_from_path()
    docstrings = extract_docstrings(source.content)
    examples = [example for docstring in docstrings for example in extract_example_code(docstring)]

    black = Black()
    args = ["black"]
    for example in examples:
        print(example)
    black.run(args, [(example, source) for example in examples])


def main() -> None:
    parser = argparse.ArgumentParser(prog="doc-pipe", description="A moe moe project")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()  # type: ignore

    create_cache_dir()
    test()


if __name__ == "__main__":
    main()

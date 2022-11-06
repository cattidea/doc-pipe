from __future__ import annotations

import argparse
import inspect

from doc_pipe import __version__
from doc_pipe.helpers.docstring import extract_docstrings
from doc_pipe.helpers.example_code import extract_example_code


def test():
    source = """
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

        b = 2
        print(b)
        ```
        '''
        pass

    """
    source = inspect.cleandoc(source)
    docstrings = extract_docstrings(source)
    for docstring in docstrings:
        for example_code in extract_example_code(docstring):
            print(example_code)


def main() -> None:
    parser = argparse.ArgumentParser(prog="doc-pipe", description="A moe moe project")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()  # type: ignore

    test()


if __name__ == "__main__":
    main()

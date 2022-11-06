from __future__ import annotations


class Pipe:
    def __init__(self, name: str):
        ...


class CommonPipe(Pipe):
    def __init__(self):
        super().__init__("CommonPipe")

    # def

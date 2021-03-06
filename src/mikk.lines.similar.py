import sys
from typing import TypeVar, Set, List, Tuple

import click


T = TypeVar("T")

translation = str.maketrans({
    "_": " ",
    "-": " ",
    ",": " ",
    "!": " ",
    ".": " ",
    "'": " ",
    "(": " ",
    ")": " ",
    "[": " ",
    "]": " ",
    "@": " ",
    "&": " ",
    "#": " ",
    "+": " ",
    "=": " ",
    "|": " ",
    "~": " ",
})


def to_words(string: str):
    out = string.translate(translation)

    return {i for i in out.split(" ") if i and i != " "}


class Point:
    def __init__(self, index: int, string: str):
        self.index = index
        self.string = string
        self.words = to_words(string)


@click.command()
@click.option("--count", default=-1)
def main(count: int):

    points: List[Point] = [
        Point(i, line.rstrip())
        for i, line in enumerate(sys.stdin, 1)
    ]

    connections: List[Tuple[Point, Point, Set[str]]] = []

    offset = 1
    for i in points:
        for j in points[offset:]:
            connections.append((i, j, i.words & j.words))
        offset += 1

    connections = sorted(
        filter(lambda x: bool(x[2]), connections),
        key=lambda x: len(x[2]) / (min(len(x[0].words), len(x[1].words)) or 1),
        reverse=True
    )[:count]

    separator = "=" * 32
    print(separator)
    for a, b, intersection in connections:
        print(f"{a.index: <4} | {a.string}")
        print(f"{b.index: <4} | {b.string}")
        print(intersection)

        print(separator)


if __name__ == "__main__":
    main()

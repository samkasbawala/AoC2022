from __future__ import annotations
from typing import List

import os

import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
A Y
B X
C Z
"""

EXPECTED = 15


def solve(input_long: str) -> int:
    games: List[str] = [game for game in input_long.split("\n") if len(game) > 0]

    win = {"A": "Y", "B": "Z", "C": "X"}
    pts = {"X": 1, "Y": 2, "Z": 3}

    total = 0
    for game in games:
        elf, me = game.split(" ")

        # We win
        if win[elf] == me:
            total += 6

        # Tie
        elif ord(elf) + 23 == ord(me):
            total += 3

        total += pts[me]

    return total


@pytest.mark.parametrize(
    ("input_sample", "expected"),
    ((INPUT_SAMPLE, EXPECTED),),
)
def test(input_sample: str, expected: int):
    assert solve(input_sample) == expected


def main() -> None:
    with open(INPUT, "r") as file:
        print(solve(file.read()))


if __name__ == "__main__":
    main()

from __future__ import annotations

import os
from typing import Tuple
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

EXPECTED = 13


def solve(input_long: str) -> int:
    simulation = [line for line in input_long.splitlines()]

    visited = {(0, 0)}
    head = (0, 0)
    tail = (0, 0)

    for move in simulation:
        direction, distance = move.split()

        for _ in range(int(distance)):

            if direction.lower() == "r":
                head = (head[0] + 1, head[1])
            elif direction.lower() == "l":
                head = (head[0] - 1, head[1])
            elif direction.lower() == "u":
                head = (head[0], head[1] + 1)
            else:
                head = (head[0], head[1] - 1)

            tail = fix(head, tail)
            visited.add(tail)

    return len(visited)


def fix(head: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:
    dx = abs(head[0] - tail[0])
    dy = abs(head[1] - tail[1])

    if dx >= 2:
        return (tail[0] + 1 if tail[0] < head[0] else tail[0] - 1, head[1])

    if dy >= 2:
        return (head[0], tail[1] + 1 if tail[1] < head[1] else tail[1] - 1)

    return tail


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

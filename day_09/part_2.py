from __future__ import annotations

import os
from typing import Tuple
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

EXPECTED = 36


def solve(input_long: str) -> int:
    simulation = [line for line in input_long.splitlines()]

    visited = {(0, 0)}
    knots = [(0, 0) for _ in range(10)]

    for move in simulation:
        direction, distance = move.split()

        for _ in range(int(distance)):

            head = knots[0]
            if direction.lower() == "r":
                knots[0] = (head[0] + 1, head[1])
            elif direction.lower() == "l":
                knots[0] = (head[0] - 1, head[1])
            elif direction.lower() == "u":
                knots[0] = (head[0], head[1] + 1)
            else:
                knots[0] = (head[0], head[1] - 1)

            for idx, knot in enumerate(knots[1::], 1):
                knots[idx] = fix(knots[idx - 1], knot)

            visited.add(knots[-1])

    return len(visited)


def fix(head: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:
    dx = abs(head[0] - tail[0])
    dy = abs(head[1] - tail[1])

    # Took me forever to find this case, omg, happens in part 2 but not in part 1
    if dx >= 2 and dy >= 2:
        return (
            head[0] - 1 if tail[0] < head[0] else head[0] + 1,
            head[1] - 1 if tail[1] < head[1] else head[1] + 1,
        )

    if dx >= 2:
        return (head[0] - 1 if tail[0] < head[0] else head[0] + 1, head[1])

    if dy >= 2:
        return (head[0], head[1] - 1 if tail[1] < head[1] else head[1] + 1)

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

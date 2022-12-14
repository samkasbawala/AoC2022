from __future__ import annotations

import os
from typing import Set, Tuple
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

EXPECTED = 24


def solve(input_long: str) -> int:
    rocks = [
        rock_path.split("->")
        for rock_path in [path.strip() for path in input_long.splitlines()]
    ]

    # Settled items
    settled: Set[Tuple[int, int]] = set()
    max_y = -float("inf")

    # Get all rock coords, and get max depth until void
    for path in rocks:
        idx = 1
        path_clean = [item.strip() for item in path]

        while idx < len(path_clean):
            x1, y1 = (int(i) for i in path_clean[idx - 1].split(","))
            x2, y2 = (int(i) for i in path_clean[idx].split(","))

            max_y = max(max_y, y1, y2)

            if x1 == x2:
                for y3 in range(min(y1, y2), max(y1, y2) + 1):
                    settled.add((x1, y3))
            else:
                for x3 in range(min(x1, x2), max(x1, x2) + 1):
                    settled.add((x3, y1))

            idx += 1

    sand_fallen = 0
    while True:
        new_sand = move_particle((500, 0), settled, max_y)

        # Void reached if new_sand is None
        if not new_sand:
            return sand_fallen

        settled.add(new_sand)
        sand_fallen += 1


def move_particle(
    particle_pos: Tuple[int, int],
    settled: Set[Tuple[int, int]],
    max_y: float,
):
    x, y = particle_pos

    # We have reached the void
    if y >= max_y:
        return None

    if (x, y + 1) not in settled:
        return move_particle((x, y + 1), settled, max_y)
    elif (x - 1, y + 1) not in settled:
        return move_particle((x - 1, y + 1), settled, max_y)
    elif (x + 1, y + 1) not in settled:
        return move_particle((x + 1, y + 1), settled, max_y)

    return particle_pos


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

from __future__ import annotations

import os
import numpy as np
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
30373
25512
65332
33549
35390
"""

EXPECTED = 21


def solve(input_long: str) -> int:
    grid = np.array([[int(num) for num in line] for line in input_long.splitlines()])

    max_score = -float("inf")

    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            height = grid[i, j]

            down = get_distance(height, grid[i + 1 :, j])
            top = get_distance(height, grid[i - 1 :: -1, j])
            left = get_distance(height, grid[i, j - 1 :: -1])
            right = get_distance(height, grid[i, j + 1 :])

            max_score = max(max_score, down * top * left * right)

    return int(max_score)


def get_distance(height: int, array: np.ndarray) -> int:
    distance = 0
    for item in array:
        if item >= height:
            return distance + 1
        distance += 1
    return distance


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

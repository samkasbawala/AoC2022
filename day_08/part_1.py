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

    visible = grid.shape[0] * 2 + (grid.shape[1] - 2) * 2

    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            down = np.max(grid[i + 1 :, j])
            top = np.max(grid[:i, j])
            left = np.max(grid[i, :j])
            right = np.max(grid[i, j + 1 :])

            visible += 1 if grid[i, j] > min(down, top, left, right) else 0

    return visible


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

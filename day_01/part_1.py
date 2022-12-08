from __future__ import annotations
from typing import List

import os

import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

EXPECTED = 24000


def solve(input_long: str) -> int:
    elves: List[str] = [elf for elf in input_long.split("\n\n")]
    cals: List[int] = [sum(int(cal) for cal in elf.splitlines()) for elf in elves]

    return max(cals)


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

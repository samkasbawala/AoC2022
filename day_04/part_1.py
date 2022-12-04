from __future__ import annotations

import os

import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

EXPECTED = 2


def solve(input: str) -> int:
    assignments = [assignment for assignment in input.splitlines()]

    total = 0
    for assignment in assignments:
        elf_1, elf_2 = assignment.split(",")
        elf_1_range = [int(num) for num in elf_1.split("-")]
        elf_2_range = [int(num) for num in elf_2.split("-")]

        elf_1_set = set(range(elf_1_range[0], elf_1_range[1] + 1))
        elf_2_set = set(range(elf_2_range[0], elf_2_range[1] + 1))

        if (
            elf_1_set.intersection(elf_2_set) == elf_1_set
            or elf_2_set.intersection(elf_1_set) == elf_2_set
        ):
            total += 1

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

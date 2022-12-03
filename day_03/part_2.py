from __future__ import annotations

import os

import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

EXPECTED = 70


def solve(input: str) -> int:
    rucksacks = [rucksack for rucksack in input.splitlines()]
    priorities_lower_case = {
        chr(num): num - ord("a") + 1 for num in range(ord("a"), ord("z") + 1)
    }

    priorities_upper_case = {
        chr(num): num - ord("A") + 27 for num in range(ord("A"), ord("Z") + 1)
    }

    total = 0
    for i in range(0, len(rucksacks) - 2, 3):
        item = (
            set([ch for ch in rucksacks[i]])
            .intersection(set([ch for ch in rucksacks[i + 1]]))
            .intersection(set([ch for ch in rucksacks[i + 2]]))
        )
        for ch in item:
            total += priorities_lower_case.get(ch, 0) + priorities_upper_case.get(ch, 0)

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

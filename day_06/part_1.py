from __future__ import annotations

import os
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""

EXPECTED = 7


def solve(input_long: str) -> int:
    message = input_long.strip()

    for idx in range(0, len(message) - 4):
        sub_set = set(message[idx : idx + 4])
        if len(sub_set) == 4:
            return idx + 4

    return -1


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

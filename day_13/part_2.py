from __future__ import annotations
import ast
import functools
import itertools

import os
from typing import Any, List
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

EXPECTED = 140


def solve(input_long: str) -> int:
    packets = [
        ast.literal_eval(line.strip())
        for line in input_long.replace("\n\n", "\n").split()
    ]

    packets.append([[2]])
    packets.append([[6]])

    # https://stackoverflow.com/questions/32752739/how-does-the-functools-cmp-to-key-function-work
    packets.sort(key=functools.cmp_to_key(compare))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


def compare(left: List[Any] | int, right: List[Any] | int) -> int:
    # Return 0 when the items are the same, meaning that we need to recurse

    if isinstance(left, int) and not isinstance(right, int):
        left = [left]
    if isinstance(right, int) and not isinstance(left, int):
        right = [right]

    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if isinstance(left, list) and isinstance(right, list):
        for l, r in itertools.zip_longest(left, right):
            if l is None:
                return -1
            elif r is None:
                return 1

            verdict = compare(l, r)
            if verdict != 0:
                return verdict

        return 0

    # Cannot get here, we covered all cases above
    return 0


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

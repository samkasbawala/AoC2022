from __future__ import annotations
import ast
import itertools

import os
from typing import Any, List, Optional
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

EXPECTED = 13


def solve(input_long: str) -> int:
    packets = [
        pair.split() for pair in [packet.strip() for packet in input_long.split("\n\n")]
    ]

    total = 0
    for idx, (left, right) in enumerate(packets, 1):
        # https://stackoverflow.com/questions/1894269/how-to-convert-string-representation-of-list-to-a-list
        pair_result = compare(ast.literal_eval(left), ast.literal_eval(right))

        # If pair_result is None, means both left and right are the same, thus valid
        total += idx if (pair_result or pair_result is None) else 0

    return total


def compare(left: List[Any] | int, right: List[Any] | int) -> Optional[bool]:
    # Return 'None' when the items are the same, meaning that we need to recurse

    if isinstance(left, int) and not isinstance(right, int):
        left = [left]
    if isinstance(right, int) and not isinstance(left, int):
        right = [right]

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if isinstance(left, list) and isinstance(right, list):
        for l, r in itertools.zip_longest(left, right):
            if l is None:
                return True
            elif r is None:
                return False

            verdict = compare(l, r)
            if verdict is not None:
                return verdict

        return None

    # Cannot get here, we covered all cases above
    return None


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

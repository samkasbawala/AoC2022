from __future__ import annotations

from collections import deque
import os
from typing import Deque, List

import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

EXPECTED = "MCD"


def solve(input: str) -> str:
    first, procedure = [parts for parts in input.split("\n\n")]
    layers = first.splitlines()

    # Create a stack (ds) for each stack in the problem
    stacks: List[Deque[str]] = [deque() for _ in layers[-1].split()]

    # Add the crates to the stack
    for layer in layers[: len(layers) - 1]:
        for idx, char in enumerate(layer[1::4]):
            if not char.isspace():
                stacks[idx].append(char)

    # Parse moves
    moves = [
        (int(move[1]), int(move[3]) - 1, int(move[5]) - 1)
        for move in [move.split() for move in [line for line in procedure.splitlines()]]
    ]

    # Loop through the moves
    for count, source, dest in moves:
        temp: Deque[str] = deque()
        for _ in range(count):
            item = stacks[source].popleft()
            temp.append(item)

        for _ in range(count):
            item = temp.pop()
            stacks[dest].appendleft(item)

    # Join the string, pop from the stack if the stack is non empty
    return "".join([stack.popleft() for stack in stacks if stack])


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

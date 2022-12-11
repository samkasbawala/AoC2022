from __future__ import annotations
from collections import deque

import os
from typing import List, Tuple
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

EXPECTED = 10605


class Monkey:
    def __init__(
        self,
        queue: List[int],
        operation: Tuple[str, ...],
        test: int,
        monkey_1: int,
        monkey_2: int,
    ) -> None:
        self.queue = deque(queue)
        self.operation = operation
        self.test = test
        self.test_true = monkey_1
        self.test_false = monkey_2
        self.inspected = 0

    def do_operation(self, item: int) -> int:
        value = item if self.operation[1] == "old" else int(self.operation[1])

        if self.operation[0] == "+":
            return item + value

        return item * value


def solve(input_long: str) -> int:
    monkey_descriptions = [line for line in input_long.split("\n\n")]
    monkey_list: List[Monkey] = []

    # Initialize monkeys
    for description in monkey_descriptions:
        lines = [line.strip() for line in description.splitlines()]
        items = [
            int(num)
            for num in lines[1].replace("Starting items:", "").strip().split(",")
        ]
        operation = tuple(lines[2].replace("Operation: new = old", "").strip().split())
        test = int(lines[3].replace("Test: divisible by", "").strip())
        monkey_1 = int(lines[4].replace("If true: throw to monkey", "").strip())
        monkey_2 = int(lines[5].replace("If false: throw to monkey", "").strip())

        monkey_list.append(
            Monkey(
                items,
                operation,
                test,
                monkey_1,
                monkey_2,
            )
        )

    # Do rounds
    for _ in range(20):
        for monkey in monkey_list:
            while monkey.queue:
                item = monkey.queue.popleft()
                monkey.inspected += 1
                new_item = monkey.do_operation(item) // 3

                true_monkey = monkey_list[monkey.test_true]
                false_monkey = monkey_list[monkey.test_false]

                true_monkey.queue.append(
                    new_item
                ) if new_item % monkey.test == 0 else false_monkey.queue.append(
                    new_item
                )

    monkey_list_inspected = [
        monkey.inspected for monkey in sorted(monkey_list, key=lambda x: x.inspected)
    ]

    return monkey_list_inspected[-1] * monkey_list_inspected[-2]


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

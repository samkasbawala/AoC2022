from __future__ import annotations

import os
from typing import Dict, List, Optional, Set
import pytest

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

EXPECTED = 24933642


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.files: Dict[str, int] = {}
        self.dirs: Dict[str, Node] = {}
        self.parent: Optional[Node] = None
        self.size: int = 0


def solve(input_long: str) -> int:
    outputs = [output.strip() for output in input_long.split("\n$")]

    root = Node("/")
    current_folder = root

    for output in outputs[1::]:
        lines = output.splitlines()
        command = lines[0]

        # Change dir command
        if command.startswith("cd"):
            next_dir: str = command[2::].strip()

            if next_dir == ".." and current_folder.parent is not None:
                current_folder = current_folder.parent
            else:
                current_folder = current_folder.dirs[next_dir]

        # ls command
        else:
            for rest in lines[1::]:

                # Directory
                if rest.startswith("dir"):
                    new_folder_name = rest[3::].strip()
                    new_folder = Node(new_folder_name)
                    current_folder.dirs[new_folder_name] = new_folder

                    new_folder.parent = current_folder

                # File
                else:
                    size, name = rest.split()
                    current_folder.files[name.strip()] = int(size.strip())

    get_sizes(root)
    space_free = 70000000 - root.size
    space_needed = 30000000 - space_free

    return dfs_dirs(root, space_needed)


def get_sizes(node: Node) -> None:
    if len(node.dirs) > 0:
        for child in node.dirs.values():
            get_sizes(child)

        node.size = sum([child.size for child in node.dirs.values()])

    node.size += sum(node.files.values())


def dfs_dirs(root: Node, space_needed: int) -> int:

    stack: List[Node] = []
    visited: Set[Node] = set()
    stack.append(root)
    total = float("inf")

    while stack:
        node = stack.pop()

        visited.add(node)

        for child in node.dirs.values():
            if child not in visited:
                stack.append(child)

        total = min(total, node.size) if node.size > space_needed else total

    return int(total)


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

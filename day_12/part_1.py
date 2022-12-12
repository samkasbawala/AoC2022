from __future__ import annotations
from collections import defaultdict

import os
from typing import Dict, List, NamedTuple, Optional, Tuple
import numpy as np
import pytest
import heapq as heap

INPUT = os.path.join(os.path.dirname(__file__), "input.txt")

INPUT_SAMPLE = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

EXPECTED = 31


class Node(NamedTuple):
    value: str
    neighbors: List[Tuple[int, int]]


def solve(input_long: str) -> Optional[int]:
    grid = np.array(
        [
            [ord(char) for char in line.strip()]
            for line in input_long.split("\n")
            if len(line.strip()) > 0
        ]
    )

    graph: Dict[Tuple[int, int], Node] = {}
    m, n = grid.shape

    start: Tuple[int, int]
    end: Tuple[int, int]

    # Initialize Graph
    for x in range(m):
        for y in range(n):
            value = grid[x, y]

            if value == ord("S"):
                start = (x, y)
                grid[x, y] = ord("a")

            elif value == ord("E"):
                end = (x, y)
                grid[x, y] = ord("z")

    for x in range(m):
        for y in range(n):
            value = grid[x, y]

            neighbors = [
                neighbor
                for neighbor in get_neighbors(x, y, m, n)
                if grid[neighbor] <= value + 1
            ]
            graph[(x, y)] = graph.get((x, y), Node(value=value, neighbors=neighbors))

    # Dijkstra
    answer = dijkstra(graph, start, end)
    return int(answer) if answer is not None else answer


def get_neighbors(x: int, y: int, m: int, n: int) -> List[Tuple[int, int]]:
    neighbors = [
        (new_x, new_y)
        for new_x, new_y in {(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)}
        if (new_x >= 0 and new_x < m) and (new_y >= 0 and new_y < n)
    ]

    return neighbors


def dijkstra(
    graph: Dict[Tuple[int, int], Node],
    source: Tuple[int, int],
    target: Tuple[int, int],
) -> Optional[float]:

    visited = set()
    pq: List[Tuple[int, Tuple[int, int]]] = []
    dist: defaultdict[Tuple[int, int], float] = defaultdict(lambda: float("inf"))

    dist[source] = 0
    heap.heappush(pq, (0, source))

    while pq:
        _, u = heap.heappop(pq)

        if u == target:
            return dist[u]
        visited.add(u)

        for neighbor in graph[u].neighbors:
            if neighbor in visited:
                continue

            alt = dist[u] + 1
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                heap.heappush(pq, (alt, neighbor))

    return


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

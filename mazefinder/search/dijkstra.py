"""Support for a Dijkstra state space search algorithm."""

from math import inf
from mazefinder.animate import Animator
from mazefinder.problem import MazeProblem, Position
from .data_structures import Heap


def dijkstra(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """Search through the state space using Dijskstra's algorithm."""
    heap: Heap[Position] = Heap([(0, problem.initial)])
    distances: dict[Position, float] = {problem.initial: 0}
    previous: dict[Position, Position] = {}

    while heap:
        distance, current = heap.pop()
        if problem.is_goal(current):
            return problem.reconstruct_path(previous), len(distances)
        for weight, neighbor in problem.adjacent_weighted(current):
            total = distance + weight
            if total < distances.get(neighbor, inf):
                distances[neighbor] = total
                previous[neighbor] = current
                problem.grid.visit(neighbor)
                animator.next_frame(problem.grid)
                heap.push(total, neighbor)

    return None, len(distances)

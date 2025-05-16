"""Support for A* state space search algorithms."""

from math import inf
from mazefinder.animate import Animator
from mazefinder.problem import MazeProblem, Position
from .data_structures import Heap


def a_star(
    problem: MazeProblem,
    animator: Animator,
    method: str = "manhattan",
    weight: float = 1,
) -> tuple[list[Position] | None, int]:
    """Search through the state space using Dijskstra's algorithm."""
    heap: Heap[Position] = Heap([(0, problem.initial)])
    distances: dict[Position, float] = {problem.initial: 0}
    previous: dict[Position, Position] = {}

    while heap:
        _, current = heap.pop()
        if problem.is_goal(current):
            return problem.reconstruct_path(previous), len(distances)
        distance = distances[current]
        for neighbor in problem.adjacent(current):
            total = distance + 1
            if total < distances.get(neighbor, inf):
                distances[neighbor] = total
                previous[neighbor] = current
                problem.grid.visit(neighbor)
                animator.next_frame(problem.grid)

                if method == "manhattan":
                    heap.push(total + problem.manhattan(neighbor) * weight, neighbor)
                elif method == "euclidean":
                    heap.push(total + problem.euclidean(neighbor) * weight, neighbor)
                else:
                    raise NotImplementedError(
                        "choose either 'manhattan' or 'euclidean' as method"
                    )

    return None, len(distances)


def a_star_manhattan(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """A* algorithm using manhattan distance."""
    return a_star(problem, animator, method="manhattan")


def a_star_euclidean(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """A* algorithm using euclidean distance."""
    return a_star(problem, animator, method="euclidean")


def a_star_overweight_manhattan(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """A* algorithm with an overweight manhattan heurestic."""
    return a_star(problem, animator, method="manhattan", weight=1.5)


def a_star_overweight_euclidean(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """A* algorithm with an overweight euclidean heurestic."""
    return a_star(problem, animator, method="euclidean", weight=1.5)

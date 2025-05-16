"""Support for a greedy state space search algorithm."""

from mazefinder.animate import Animator
from mazefinder.problem import MazeProblem, Position
from .data_structures import Heap


def greedy(
    problem: MazeProblem, animator: Animator, method: str = "manhattan"
) -> tuple[list[Position] | None, int]:
    """Search through the state space using a Greedy algorithm."""
    heap: Heap[Position] = Heap([(0, problem.initial)])
    visited: set[Position] = {problem.initial}
    previous: dict[Position, Position] = {}

    while heap:
        _, current = heap.pop()
        if problem.is_goal(current):
            return problem.reconstruct_path(previous), len(visited)
        for neighbor in problem.adjacent(current):
            if neighbor not in visited:
                visited.add(neighbor)
                problem.grid.visit(neighbor)
                animator.next_frame(problem.grid)
                previous[neighbor] = current

                if method == "manhattan":
                    heap.push(problem.manhattan(neighbor), neighbor)
                elif method == "euclidean":
                    heap.push(problem.euclidean(neighbor), neighbor)
                else:
                    raise NotImplementedError(
                        "choose either 'manhattan' or 'euclidean' as method"
                    )

    return None, len(visited)


def greedy_manhattan(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """Greedy algorithm using manhattan distance."""
    return greedy(problem, animator, method="manhattan")


def greedy_euclidean(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """Greedy algorithm using euclidean distance."""
    return greedy(problem, animator, method="euclidean")

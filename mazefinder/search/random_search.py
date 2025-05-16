"""Support for a random-first state space search algorithm."""

from mazefinder.problem import MazeProblem, Position
from mazefinder.animate import Animator
from .data_structures import RandomList


def random_search(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """Search through state space using Random-first Search."""
    random_list: RandomList[Position] = RandomList([problem.initial])
    previous: dict[Position, Position] = {}
    visited: set[Position] = {problem.initial}

    while random_list:
        current = random_list.pop()
        if problem.is_goal(current):
            return problem.reconstruct_path(previous), len(visited)

        for neighbor in problem.adjacent(current):
            if neighbor not in visited:
                visited.add(neighbor)
                problem.grid.visit(neighbor)
                animator.next_frame(problem.grid)
                random_list.push(neighbor)
                previous[neighbor] = current

    return None, len(visited)

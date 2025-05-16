"""Support for depth-first state space search algorithms."""

from typing import Iterator
from mazefinder.problem import Position, MazeProblem
from mazefinder.animate import Animator
from .data_structures import Stack


def recursive_dfs(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """Search through state space using recursive Depth-First Search."""
    visited: set[Position] = set()
    previous: dict[Position, Position] = {}

    def search(current: Position) -> bool:
        """Recursive search element that returns whether a path to end was found."""
        visited.add(current)
        problem.grid.visit(current)
        animator.next_frame(problem.grid)
        if problem.is_goal(current):
            return True
        for neighbor in problem.adjacent(current):
            if neighbor not in visited:
                previous[neighbor] = current
                if search(neighbor):
                    return True
        return False

    try:
        if search(problem.initial):
            return problem.reconstruct_path(previous), len(visited)
    except RecursionError:
        print("Recursion depth exceeded. Maze is too deep for the current stack limit.")

    return None, len(visited)


def stack_dfs(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """Search through state space using explicit stack Depth-First Search."""
    stack: Stack[Position] = Stack([problem.initial])
    visited: set[Position] = set()
    previous: dict[Position, Position] = {}

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        problem.grid.visit(current)
        if problem.is_goal(current):
            return problem.reconstruct_path(previous), len(visited)
        animator.next_frame(problem.grid)
        for neighbor in problem.adjacent(current):
            if neighbor not in visited:
                previous[neighbor] = current
                stack.push(neighbor)

    return None, len(visited)


def iterator_dfs(
    problem: MazeProblem, animator: Animator
) -> tuple[list[Position] | None, int]:
    """Search through the state space using iterator Depth-First Search."""

    stack: Stack[tuple[Position, Iterator[Position]]] = Stack(
        [(problem.initial, problem.adjacent(problem.initial))]
    )
    visited: set[Position] = {problem.initial}
    previous: dict[Position, Position] = {}

    if problem.is_goal(problem.initial):
        return problem.reconstruct_path(previous), len(visited)

    while stack:
        predecessor, children = stack.peek()
        current = next(children, None)
        if current is None:
            stack.pop()
            continue

        if current not in visited:
            visited.add(current)
            problem.grid.visit(current)
            animator.next_frame(problem.grid)
            previous[current] = predecessor
            if problem.is_goal(current):
                return problem.reconstruct_path(previous), len(visited)
            stack.push((current, problem.adjacent(current)))

    return None, len(visited)

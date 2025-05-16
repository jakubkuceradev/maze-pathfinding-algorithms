"""Support for a breadth-first state space search algorithms."""

from mazefinder.problem import Position, MazeProblem, ROOT
from mazefinder.animate import Animator
from .data_structures import Queue


def bfs(problem: MazeProblem, animator: Animator) -> tuple[list[Position] | None, int]:
    """Search through the state space using Breadth-First Search."""
    queue: Queue[Position] = Queue([problem.initial])
    previous: dict[Position, Position] = {}
    visited: set[Position] = {problem.initial}  # open and closed set union

    while queue:
        current = queue.pop()
        if problem.is_goal(current):
            return problem.reconstruct_path(previous), len(visited)
        for neighbor in problem.adjacent(current):
            if neighbor not in visited:
                visited.add(neighbor)
                problem.grid.visit(neighbor)
                animator.next_frame(problem.grid)
                queue.push(neighbor)
                previous[neighbor] = current

    return None, len(visited)

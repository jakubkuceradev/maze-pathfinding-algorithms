"""Defines the abstract and concrete formal problem."""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
import math
import re


@dataclass(frozen=True)
class State(ABC):
    """Defines a state in the problem."""


@dataclass(frozen=True)
class Position(State):
    """Defines the position of a cell"""

    column: int
    row: int

    def __add__(self, other):
        """Defines addition for positions"""
        if isinstance(other, Position):
            return Position(
                column=self.column + other.column,
                row=self.row + other.row,
            )
        raise NotImplementedError

    def __repr__(self):
        """Define string representation"""
        return f"[{self.column},{self.row}]"


ROOT = Position(-1, -1)


class Move(Enum):
    "Possible moves in a 2D grid. (column, row)"

    UP = Position(1, 0)
    DOWN = Position(-1, 0)
    LEFT = Position(0, -1)
    RIGHT = Position(0, 1)


class Cell(Enum):
    "Possible states of a cell in a 2D grid."

    WALL = "\033[0m██"  # white block
    PATH = "\033[0;32m██"  # green block
    EMPTY = "  "  # empty space
    OPEN = "\033[1;34m▒▒"  # blue mesh
    START = "\033[1;32mST"  # green 'S'
    END = "\033[1;32mEN"  # green 'E


@dataclass
class Grid:
    """Defines the state-space for a grid"""

    data: list[list[Cell]]

    def visit(self, position: Position) -> None:
        """Set a cell in a grid as visited."""
        if self.data[position.row][position.column] not in (Cell.START, Cell.END):
            self.data[position.row][position.column] = Cell.OPEN

    def path(self, position: Position) -> None:
        """Set a cell as a part of the path."""
        if self.data[position.row][position.column] not in (Cell.START, Cell.END):
            self.data[position.row][position.column] = Cell.PATH

    def get(self, position: Position) -> Cell:
        """Get the value of a cell in a grid."""
        return self.data[position.row][position.column]

    def wall(self, position: Position) -> bool:
        """Returns true if there is a wall at the position."""
        return self.get(position) == Cell.WALL


@dataclass()
class Problem(ABC):
    """The abstract class for a formal problem"""

    initial: State
    goal: State

    @abstractmethod
    def actions(self, state):
        """Return permissible actions for a state."""
        raise NotImplementedError

    @abstractmethod
    def result(self, state, action):
        """Return the resulting state for a given action and state."""
        raise NotImplementedError

    @abstractmethod
    def is_goal(self, state):
        """Returns true if state is the goal of the problem"""
        raise NotImplementedError


@dataclass
class MazeProblem(Problem):
    """Specification of the maze problem."""

    initial: Position
    goal: Position
    grid: Grid

    def actions(self, state: Position):
        """Return permissible moves for a state."""
        return (move for move in Move if not self.grid.wall(state + move.value))

    def result(self, state: Position, action: Move) -> Position:
        """Return the resulting position for a given move and state."""
        return state + action.value

    def adjacent(self, state: Position):
        """Return adjacent positions to a given state."""
        return (self.result(state, action) for action in self.actions(state))

    def adjacent_weighted(self, state: Position):
        """Return adjacent positions with added dummy weight."""
        return ((1.0, self.result(state, action)) for action in self.actions(state))

    def manhattan(self, state: Position) -> float:
        """Calculate the manhattan distance of a state from goal."""
        return abs(state.column - self.goal.column) + abs(state.row - self.goal.row)

    def euclidean(self, state: Position) -> float:
        """Calculate the manhattan distance of a state from goal."""
        return math.sqrt(
            (state.column - self.goal.column) ** 2 + (state.row - self.goal.row) ** 2
        )

    def is_goal(self, state):
        """Returns True if state is the position of maze end."""
        return state == self.goal

    def reconstruct_path(self, previous: dict[Position, Position]):
        """Return a permissible solution to the maze problem."""
        path = [self.goal]
        if self.goal == self.initial:
            return path
        current = previous[self.goal]
        while current != self.initial:
            path.append(current)
            self.grid.path(current)
            current = previous[current]
        path.append(self.initial)
        return path[::-1]


def load_problem(
    file_path: str,
) -> MazeProblem:
    """Reads and parses file at 'path' and returns a maze problem."""

    with open(file_path, encoding="utf-8") as file:
        text = file.read()

    lines = text.strip().splitlines()

    data = [
        [Cell.WALL if char == "X" else Cell.EMPTY for char in line.strip()]
        for line in lines[:-2]
    ]

    start_match = re.match(r"^start\D+(\d+)\D+(\d+)$", lines[-2])
    end_match = re.match(r"^end\D+(\d+)\D+(\d+)$", lines[-1])

    if not start_match or not end_match:
        raise ValueError("file input needs to end with start and end coordinates")

    start = Position(column=int(start_match.group(1)), row=int(start_match.group(2)))
    end = Position(column=int(end_match.group(1)), row=int(end_match.group(2)))

    data[start.row][start.column] = Cell.START
    data[end.row][end.column] = Cell.END

    return MazeProblem(start, end, Grid(data))

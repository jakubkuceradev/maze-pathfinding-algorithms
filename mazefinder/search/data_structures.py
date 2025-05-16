"""Support for generic queue-like datastructures."""

from dataclasses import dataclass, field
from heapq import heappop, heappush, heapify
from collections import deque
from random import randint
from typing import TypeVar, Generic, Iterable

T = TypeVar("T")  # Generic type variable


@dataclass
class DistanceItem(Generic[T]):
    """An item intended to be used in a heap data structure."""

    distance: float
    item: T = field(compare=False)

    def __lt__(self, other):
        """Return whether self is lower than other."""
        if isinstance(other, DistanceItem):
            return self.distance < other.distance
        return NotImplementedError

    def __iter__(self):
        """Returns an iterator of the class fields."""
        return iter((self.distance, self.item))


@dataclass
class Heap(Generic[T]):
    """Heap used for implementing a priority queue."""

    items: list[DistanceItem[T]]

    def __init__(self, items: Iterable[T] = ()):
        """Initialize the queue with optional items."""
        self.items = [DistanceItem(item[0], item[1]) for item in items]
        heapify(self.items)

    def pop(self) -> DistanceItem[T]:
        """Pop the item with lowest distance."""
        return heappop(self.items)

    def push(self, distance: float, item: T):
        """Push an item into the heap."""
        heappush(self.items, DistanceItem(distance, item))

    def __len__(self):
        return len(self.items)


@dataclass
class Queue(Generic[T]):
    """Queue interface using a deque."""

    items: deque[T] = field(init=False)

    def __init__(self, items: Iterable[T] = ()):
        """Initialize the queue with optional items."""
        self.items = deque(items)

    def push(self, item: T):
        """Push an item to queue end."""
        self.items.append(item)

    def pop(self) -> T:
        """Pop and return an item from queue beginning."""
        return self.items.popleft()

    def peek(self) -> T:
        """Return an item from queue top without popping."""
        return self.items[-1]

    def __bool__(self) -> bool:
        return bool(self.items)


@dataclass
class Stack(Generic[T]):
    """Stack interface using a deque."""

    items: deque[T] = field(init=False)

    def __init__(self, items: Iterable[T] = ()):
        """Initialize the stack with optional items."""
        self.items = deque(items)

    def push(self, item: T):
        """Push an item to stack top."""
        self.items.append(item)

    def pop(self) -> T:
        """Pop and return an item from stack top."""
        return self.items.pop()

    def peek(self) -> T:
        """Return an item from stack top without popping."""
        return self.items[-1]

    def __bool__(self) -> bool:
        return bool(self.items)


@dataclass
class RandomList(Generic[T]):
    """List interface providing fast random element access."""

    items: list[T] = field(init=False)

    def __init__(self, items: Iterable[T] = ()):
        """Initialize the list with optional items."""
        self.items = list(items)

    def push(self, item: T):
        """Push an item to list end."""
        self.items.append(item)

    def pop(self) -> T:
        """Pop and return a random item from list."""
        end_index = len(self.items) - 1
        random_index = randint(0, end_index)
        self.items[end_index], self.items[random_index] = (
            self.items[random_index],
            self.items[end_index],
        )
        return self.items.pop()

    def __bool__(self):
        return bool(self.items)

from typing import Generic, TypeVar, Deque, List
from collections import deque
from heapq import heappush, heappop
from abc import abstractmethod, ABC

T = TypeVar('T')


class Base(Generic[T], ABC):
    def __init__(self) -> None:
        self._container: Deque[T] = deque()

    @abstractmethod
    def push(self, value: T) -> None:
        """push item"""

    @abstractmethod
    def pop(self) -> T:
        """pop item"""

    @abstractmethod
    def top(self) -> T:
        """top item"""

    def __len__(self) -> int:
        return len(self._container)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({list(self._container)})'


class Stack(Base):
    def push(self, value: T) -> None:
        self._container.append(value)

    def pop(self) -> T:
        return self._container.pop()

    @property
    def top(self) -> T:
        if self:
            return self._container[-1]


class Queue(Stack):
    def pop(self) -> T:
        return self._container.popleft()

    @property
    def top(self) -> T:
        return self._container[0]



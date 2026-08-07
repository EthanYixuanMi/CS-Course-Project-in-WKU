from __future__ import annotations

from collections import deque
from typing import Deque, List, Protocol, runtime_checkable

from ..profiler.rules import TaskMeta


@runtime_checkable
class Schedulable(Protocol):
    """A minimal protocol that any task object should satisfy for strategies.

    For early prototyping we rely only on an *id* and *meta* dict. This avoids
    constraining the upstream API/DB schema. Later we can replace by a dataclass
    shared in utils.models.
    """

    id: str
    meta: TaskMeta  # includes estimated "duration", etc.


class BaseStrategy(Protocol):
    """Common interface every concrete strategy must implement."""

    name: str

    def schedule(self, queue: List[Schedulable]) -> List[Schedulable]:
        """Return a **new** list ordered by this strategy.

        The original queue should **not** be mutated to avoid side-effects.
        """


# ---------------------------------------------------------------------------
# Round-Robin Strategy
# ---------------------------------------------------------------------------


class RoundRobinStrategy:
    """Classic RR using fixed *time_slice* (quantum).

    Because this is a **cloud batch scheduler** rather than an OS time-sharing
    kernel, we interpret RR as *chunked ordering* instead of real pre-emption:

    1. Split each task into a sequence of slices of length = `time_slice`.
    2. Perform cyclic traversal producing a new execution order.

    This keeps implementation stateless/easy while preserving fairness.
    """

    name = "round_robin"

    def __init__(self, time_slice: float = 1.0) -> None:
        self.time_slice = time_slice

    # Helper -----------------------------------------------------------------
    @staticmethod
    def _required_slices(duration: float, quantum: float) -> int:
        # ceil(duration / quantum)
        return int(-(-duration // quantum))

    # API --------------------------------------------------------------------
    def schedule(self, queue: List[Schedulable]) -> List[Schedulable]:
        if not queue:
            return []

        cycle: Deque[Schedulable] = deque(queue)  # shallow copy
        output: List[Schedulable] = []
        remaining_slices = {
            t.id: self._required_slices(t.meta.get("duration", 0), self.time_slice)
            for t in queue
        }

        while cycle:
            task = cycle.popleft()
            output.append(task)
            remaining_slices[task.id] -= 1
            if remaining_slices[task.id] > 0:
                cycle.append(task)
        return output


__all__ = [
    "BaseStrategy",
    "RoundRobinStrategy",
]

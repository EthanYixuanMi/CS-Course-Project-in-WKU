from __future__ import annotations

from typing import List

from .rr import BaseStrategy, Schedulable  # reuse the shared protocols


class ShortestJobFirstStrategy(BaseStrategy):
    """Non-preemptive SJF (a.k.a. SPN) — tasks sorted by *estimated duration* ascending.

    * If a task is missing `duration`, we treat it as `inf`, letting it fall to
      the end of the queue.
    * Implementation is a simple `sorted()`; complexity O(n log n) which is
      acceptable for typical queue sizes in cloud batch scheduling.
    """

    name = "sjf"

    def schedule(self, queue: List[Schedulable]) -> List[Schedulable]:
        if not queue:
            return []

        return sorted(queue, key=lambda t: t.meta.get("duration", float("inf")))


__all__ = [
    "ShortestJobFirstStrategy",
]

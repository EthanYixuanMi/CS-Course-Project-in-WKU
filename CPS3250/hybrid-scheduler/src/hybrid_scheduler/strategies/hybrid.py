from __future__ import annotations

from typing import Dict, List

from ..profiler.rules import TaskCategory, classify_task
from .rr import BaseStrategy, Schedulable
from .rr import RoundRobinStrategy
from .sjf import ShortestJobFirstStrategy
from .edf import EarliestDeadlineFirstStrategy


class HybridStrategy(BaseStrategy):
    """Hybrid scheduler that delegates to different algorithms per category.

    Default mapping (can be overridden via `strategy_map` parameter):

    | Category              | Underlying Strategy       |
    |-----------------------|---------------------------|
    | realtime              | Earliest Deadline First   |
    | short (interactive)   | Round Robin               |
    | batch                 | Shortest Job First        |

    The merge order prioritises **realtime → short → batch** so that time-critical
    jobs are dispatched first. Within each bucket, ordering follows the chosen
    sub-strategy.
    """

    name = "hybrid"

    DEFAULT_STRATEGY_MAP: Dict[TaskCategory, BaseStrategy] = {
        TaskCategory.REALTIME: EarliestDeadlineFirstStrategy(),
        TaskCategory.SHORT: RoundRobinStrategy(time_slice=1.0),
        # For batch we sometimes prefer HRRN; here choose SJF for simplicity
        TaskCategory.BATCH: ShortestJobFirstStrategy(),
    }

    # When merging, earlier indices have higher dispatch priority
    MERGE_ORDER = [
        TaskCategory.REALTIME,
        TaskCategory.SHORT,
        TaskCategory.BATCH,
    ]

    # ---------------------------------------------------------------------
    def __init__(self, strategy_map: Dict[TaskCategory, BaseStrategy] | None = None):
        self.strategy_map = strategy_map or self.DEFAULT_STRATEGY_MAP

    # ---------------------------------------------------------------------
    def schedule(self, queue: List[Schedulable]) -> List[Schedulable]:
        if not queue:
            return []

        # 1️⃣ Bucket tasks by category
        buckets: Dict[TaskCategory, List[Schedulable]] = {
            cat: [] for cat in TaskCategory  # type: ignore[arg-type]
        }
        for task in queue:
            cat = classify_task(task.meta)  # type: ignore[arg-type]
            buckets[cat].append(task)

        # 2️⃣ Apply underlying strategy within each bucket
        ordered_buckets: Dict[TaskCategory, List[Schedulable]] = {}
        for cat, tasks in buckets.items():
            strat = self.strategy_map.get(cat)
            if strat and tasks:
                ordered_buckets[cat] = strat.schedule(tasks)
            else:
                ordered_buckets[cat] = tasks  # untouched if no strategy assigned

        # 3️⃣ Merge buckets according to priority order
        merged: List[Schedulable] = []
        for cat in self.MERGE_ORDER:
            merged.extend(ordered_buckets.get(cat, []))

        return merged


__all__ = [
    "HybridStrategy",
]

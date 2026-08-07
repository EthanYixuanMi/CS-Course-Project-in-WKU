from __future__ import annotations

from typing import List

from .rr import BaseStrategy, Schedulable


class EarliestDeadlineFirstStrategy(BaseStrategy):
    """Classic EDF: tasks sorted by **absolute deadline** ascending.

    * 只要任务提供 `deadline` 字段（Unix epoch 秒）；缺失者视为无期限 → 排到队尾。
    * 本实现为 *non-preemptive offline ordering*：调度器在任务到达队列时进行排序。
      对云批处理场景足够，可在 Hybrid 组合中用于实时 / 期限驱动负载。
    """

    name = "edf"

    def schedule(self, queue: List[Schedulable]) -> List[Schedulable]:
        if not queue:
            return []

        return sorted(
            queue,
            key=lambda t: (
                t.meta.get("deadline") is None,
                t.meta.get("deadline", float("inf")),
            ),
        )


__all__ = [
    "EarliestDeadlineFirstStrategy",
]

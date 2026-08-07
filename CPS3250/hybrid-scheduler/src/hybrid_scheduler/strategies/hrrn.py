from __future__ import annotations

import time
from typing import List

from .rr import BaseStrategy, Schedulable


class HighestResponseRatioNextStrategy(BaseStrategy):
    """HRRN = (waiting + service) / service  → choose highest first.

    * `service` 使用 `meta['duration']` 估计；若缺失则取 1.0 防止除零。
    * `waiting` = *now* − `meta['arrival']`; 若任务未提供 `arrival` 则默认 0。

    由于 HRRN 需要 *当前时刻*，调度器每次调用 `schedule()` 应传入 `now`
    时间戳（秒）。为兼容旧接口，这里额外提供 `schedule_with_now(queue, now)`。
    """

    name = "hrrn"

    # ---------------------------------------------------------------------
    @staticmethod
    def _response_ratio(task: Schedulable, now: float) -> float:
        svc = max(task.meta.get("duration", 1.0), 0.001)
        waiting = max(now - task.meta.get("arrival", now), 0.0)
        return (waiting + svc) / svc

    # ---------------------------------------------------------------------
    def schedule(self, queue: List[Schedulable]) -> List[Schedulable]:
        """Default to *current wall time* for waiting calculation."""

        now = time.time()
        return self.schedule_with_now(queue, now)

    # ---------------------------------------------------------------------
    def schedule_with_now(
        self, queue: List[Schedulable], now: float
    ) -> List[Schedulable]:
        if not queue:
            return []

        return sorted(queue, key=lambda t: self._response_ratio(t, now), reverse=True)


__all__ = [
    "HighestResponseRatioNextStrategy",
]

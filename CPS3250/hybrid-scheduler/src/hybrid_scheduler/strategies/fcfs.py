# src/hybrid_scheduler/strategies/fcfs.py
from __future__ import annotations

from typing import List

# 复用 rr.py 里已经定义好的公共接口
from .rr import BaseStrategy, Schedulable


class FirstComeFirstServeStrategy(BaseStrategy):
    """FCFS —— 按到达顺序原样派发"""

    name = "fcfs"

    def schedule(self, queue: List[Schedulable]) -> List[Schedulable]:
        # queue 本身就是到达顺序；浅拷贝以避免副作用
        return queue[:]


__all__ = ["FirstComeFirstServeStrategy"]

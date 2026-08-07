from enum import Enum
from typing import Literal, TypedDict, Union


class TaskCategory(str, Enum):
    """High-level categories used by the Hybrid Scheduler."""

    SHORT = "short"  # interactive, latency-sensitive
    BATCH = "batch"  # long-running, throughput-oriented
    REALTIME = "realtime"  # deadline-driven / hard RT


class TaskMeta(TypedDict, total=False):
    """Incoming task metadata expected from API / queue.

    * duration  – estimated runtime in **seconds** (float)
    * deadline  – epoch seconds for hard deadline, or None
    * priority  – optional user priority (int, lower = higher)
    """

    duration: float
    deadline: Union[int, None]
    priority: int


# ----------------------------- threshold knobs -----------------------------

# "短任务"的最大持续时间（秒）
SHORT_DURATION_SEC = 1.0

# 若任务提供 deadline，且距离现在不足该数值（秒）⇒ 视为 realtime
REALTIME_AHEAD_SEC = 5.0


# ----------------------------- core classifier -----------------------------


def classify_task(meta: TaskMeta) -> TaskCategory:
    """Classify a task into *short / batch / realtime*.

    Parameters
    ----------
    meta : TaskMeta
        Metadata dict. Missing keys will use default `None`.

    Returns
    -------
    TaskCategory
    """

    duration = meta.get("duration") or float("inf")
    deadline = meta.get("deadline")

    # 1) Realtime if we have a near-term deadline
    if deadline is not None:
        import time

        remaining = deadline - time.time()
        if remaining <= REALTIME_AHEAD_SEC:
            return TaskCategory.REALTIME

    # 2) Otherwise short if estimated runtime is tiny
    if duration <= SHORT_DURATION_SEC:
        return TaskCategory.SHORT

    # 3) Fallback to batch
    return TaskCategory.BATCH


# Convenience literal type for external callers
CategoryLiteral = Literal[
    TaskCategory.SHORT.value,
    TaskCategory.BATCH.value,
    TaskCategory.REALTIME.value,
]


__all__ = [
    "TaskCategory",
    "TaskMeta",
    "classify_task",
    "CategoryLiteral",
]

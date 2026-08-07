# src/hybrid_scheduler/utils/models.py
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from ..profiler.rules import TaskMeta


class Category(str, Enum):
    CPU = "CPU"  # 纯计算任务
    IO = "IO"  # I/O 密集任务
    # 后续如需扩展，在这里继续加枚举值即可


class Task(BaseModel):
    """
    单条调度任务的结构定义（由 FastAPI 自动校验）

    设计目标（方案 A）：
    - 对外 API：仍然以字段形式暴露 id / category / duration / arrival / deadline。
    - 对内策略层：统一从 `meta: TaskMeta` 中读取调度所需的关键信息：
        * meta["duration"]  → RR / SJF / HRRN
        * meta["arrival"]   → HRRN
        * meta["deadline"]  → EDF
        * meta["category"]  → profiler / hybrid 分类用
    """

    id: str = Field(..., description="唯一任务 ID")
    category: Category = Field(
        ...,
        description="任务类型，必须是 Category 枚举中的值（CPU / IO 等）",
    )
    duration: float = Field(..., gt=0, description="任务的执行时间，单位：秒（>0）")

    # 可选的到达时间 / 截止时间（Unix 时间戳，秒）
    arrival: float | None = Field(
        default=None,
        description="任务到达时间（Unix epoch 秒），若省略则视为立即到达",
    )
    deadline: float | None = Field(
        default=None,
        description="任务绝对截止时间（Unix epoch 秒），用于 EDF 调度；若省略则视为无硬截止",
    )

    # 供实验统计使用的指标（由 runner 计算）
    wait_time: float | None = Field(
        default=None,
        description="等待时间（start_time - arrival）",
    )
    turnaround: float | None = Field(
        default=None,
        description="周转时间（finish_time - arrival）",
    )

    # meta 供调度策略使用的统一元数据字典（必须满足 TaskMeta 约束）
    meta: TaskMeta = Field(
        default_factory=dict,
        description="调度策略使用的元数据（duration/arrival/deadline 等会自动写入）",
    )

    def __init__(self, **data):
        """
        在 Pydantic 完成基础校验后，将关键字段同步写入 meta：

        - duration 必写入 meta["duration"]
        - arrival 若存在，写入 meta["arrival"]
        - deadline 若存在，写入 meta["deadline"]
        - category 的枚举值写入 meta["category"]（便于 profiler / hybrid 使用）
        """
        super().__init__(**data)

        # 确保 meta 是一个可变 dict
        meta = dict(self.meta or {})

        # 统一为调度策略提供字段（以模型字段为准，覆盖 meta 中的同名字段）
        meta["duration"] = self.duration

        if self.arrival is not None:
            meta["arrival"] = self.arrival

        if self.deadline is not None:
            meta["deadline"] = self.deadline

        # 保留 category 信息，供分类/分析组件使用
        meta.setdefault("category", self.category.value)

        # 写回实例
        self.meta = meta

# src/hybrid_scheduler/main.py
from __future__ import annotations

import threading
import time
from queue import SimpleQueue
from secrets import compare_digest
from typing import Dict, List
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from .config import get_settings
from .dispatcher.dispatcher import RoundRobinDispatcher, create_mock_nodes
from .monitoring.metrics import (
    metrics_router,
    record_task_completed,
    set_queue_length,
)
from .strategies.hybrid import HybridStrategy
from .utils.models import Task

# ---------------------------------------------------------------------------

app = FastAPI(title="Hybrid Scheduler", version="0.1.0")

# ---- runtime components ---------------------------------------------------
task_queue: SimpleQueue[Task] = SimpleQueue()
strategy = HybridStrategy()
dispatcher = RoundRobinDispatcher(create_mock_nodes(3))  # 三个本地节点

# ---------------------------------------------------------------------------
# 数据模型：解析客户端提交的任务元数据
# ---------------------------------------------------------------------------


# src/hybrid_scheduler/main.py
class TaskPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str = Field(..., description="CPU / IO …")
    duration: float = Field(..., gt=0, description="预计运行时长（秒）")

    # 以下两个仍然可选
    deadline: int | None = Field(None, description="Unix epoch 截止期")
    priority: int | None = Field(None, description="数字越小越高")


# ---------------------------------------------------------------------------
# 路由
# ---------------------------------------------------------------------------


@app.get("/health")
def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


app.include_router(metrics_router)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Require X-API-Key only when API_KEY is configured.

    Local development remains convenient when no key is set. Deployments that
    leave localhost should always configure a strong key or use a proper
    identity-aware proxy.
    """

    secret = get_settings().api_key
    expected = secret.get_secret_value() if secret is not None else ""
    if not expected:
        return

    if x_api_key is None or not compare_digest(x_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )


@app.post("/submit", dependencies=[Depends(require_api_key)])
async def submit_task(payload: TaskPayload) -> Dict[str, str]:
    # Generate an opaque identifier rather than accepting a caller-provided
    # value that might contain a name, email address, or another personal ID.
    task = Task(id=str(uuid4()), **payload.model_dump())
    task_queue.put(task)
    set_queue_length(task_queue.qsize())
    return {"id": task.id, "status": "queued"}


# ---------------------------------------------------------------------------
# 后台调度线程
# ---------------------------------------------------------------------------


def scheduler_worker() -> None:
    """守护线程：批量取出队列 → 调度排序 → 轮转派发（本地模拟运行）"""
    while True:
        if task_queue.empty():
            time.sleep(0.1)
            continue

        batch: List[Task] = []
        while not task_queue.empty():
            batch.append(task_queue.get())
        set_queue_length(0)

        ordered = strategy.schedule(batch)  # type: ignore[arg-type]
        dispatcher.dispatch(ordered)

        for t in ordered:
            record_task_completed(t.category, t.meta.get("duration", 0))
            time.sleep(t.meta.get("duration", 0))  # 用 sleep 模拟真实执行时间


# 启动守护线程（进程退出时自动结束）
threading.Thread(target=scheduler_worker, daemon=True).start()

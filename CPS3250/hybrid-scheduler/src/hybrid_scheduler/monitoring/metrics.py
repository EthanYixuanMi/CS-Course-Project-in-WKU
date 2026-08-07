from __future__ import annotations

from typing import Any

from prometheus_client import (  # type: ignore[import-not-found]
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.responses import Response
from fastapi import APIRouter

__all__ = [
    "registry",
    "REQUEST_COUNTER",
    "TASK_COMPLETED_COUNTER",
    "TASK_DURATION_HISTO",
    "QUEUE_LENGTH_GAUGE",
    "metrics_router",
    "record_task_completed",
    "set_queue_length",
]

# ---------------------------------------------------------------------------
# Create dedicated registry so we don't pollute default REGISTRY when testing
# ---------------------------------------------------------------------------

registry: CollectorRegistry = CollectorRegistry(auto_describe=True)

# -------------------------- common server metrics --------------------------

REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total number of HTTP requests processed by FastAPI (labelled).",
    ["method", "path", "status"],
    registry=registry,
)

# --------------------------- scheduler metrics -----------------------------

TASK_COMPLETED_COUNTER = Counter(
    "scheduler_tasks_completed_total",
    "Count of tasks successfully executed (labelled by category).",
    ["category"],
    registry=registry,
)

TASK_DURATION_HISTO = Histogram(
    "scheduler_task_duration_seconds",
    "Task execution duration in seconds, labelled by category.",
    ["category"],
    registry=registry,
    buckets=(0.1, 0.5, 1, 2, 5, 10, 30, 60, 120, float("inf")),
)

QUEUE_LENGTH_GAUGE = Gauge(
    "scheduler_queue_length",
    "Current task queue length (pending).",
    registry=registry,
)

# ---------------------------------------------------------------------------
# Utility helpers for other modules to record events
# ---------------------------------------------------------------------------


def record_task_completed(category: Any, duration: float) -> None:

    label = category.value if hasattr(category, "value") else str(category)

    TASK_COMPLETED_COUNTER.labels(label).inc()
    TASK_DURATION_HISTO.labels(label).observe(duration)


def set_queue_length(n: int) -> None:
    QUEUE_LENGTH_GAUGE.set(n)


# ---------------------------------------------------------------------------
# FastAPI router to expose /metrics (OpenMetrics text format)
# ---------------------------------------------------------------------------

metrics_router = APIRouter()


@metrics_router.get("/metrics")
async def metrics_endpoint() -> Response:
    content = generate_latest(registry)
    return Response(content=content, media_type="text/plain; version=0.0.4")

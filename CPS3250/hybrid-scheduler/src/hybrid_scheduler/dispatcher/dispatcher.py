from __future__ import annotations

import itertools
import logging
from dataclasses import dataclass
from typing import Iterable, List, Protocol, runtime_checkable

from ..profiler.rules import TaskMeta

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Task & Node abstractions (minimal for local prototype)
# ---------------------------------------------------------------------------


@runtime_checkable
class TaskLike(Protocol):
    id: str
    meta: TaskMeta


@dataclass
class ComputeNode:
    """Simplified representation of an execution target (local process / EC2)."""

    name: str
    capacity: int = 1  # how many concurrent tasks allowed (prototype)

    def __hash__(self) -> int:  # allow set/dict usage
        return hash(self.name)


# ---------------------------------------------------------------------------
# Dispatcher implementation
# ---------------------------------------------------------------------------


class RoundRobinDispatcher:
    """Very first cut: assign tasks to nodes in round-robin order.

    * No awareness of capacity / load other than simple modulo cycling.
    * Good enough for local simulation; later replace by bin-packing + AWS SDK.
    """

    def __init__(self, nodes: Iterable[ComputeNode]):
        self._nodes: List[ComputeNode] = list(nodes)
        if not self._nodes:
            raise ValueError("Dispatcher must be initialised with ≥1 node")
        self._cyclic_nodes = itertools.cycle(self._nodes)

    # ------------------------------------------------------------------
    def dispatch(self, tasks: List[TaskLike]) -> None:
        """Iterate over tasks and "assign" each to a node.

        Current implementation just logs the decision; real version would
        trigger Docker/K8s/SSH or AWS API calls.
        """

        for task in tasks:
            node = next(self._cyclic_nodes)
            # Task identifiers can become linkable metadata. Keep routine logs
            # limited to the operational fact needed for troubleshooting.
            logger.info("Dispatch task → node %s", node.name)
            # TODO: container run / boto3 ECS run_task ...


# Convenience helper to create mock nodes for unit tests


def create_mock_nodes(n: int) -> List[ComputeNode]:
    return [ComputeNode(name=f"node-{i}") for i in range(n)]


__all__ = [
    "ComputeNode",
    "RoundRobinDispatcher",
    "create_mock_nodes",
]

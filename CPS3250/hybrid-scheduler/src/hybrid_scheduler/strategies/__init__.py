# src/hybrid_scheduler/strategies/__init__.py
from .rr import RoundRobinStrategy
from .sjf import ShortestJobFirstStrategy
from .hrrn import HighestResponseRatioNextStrategy
from .edf import EarliestDeadlineFirstStrategy
from .hybrid import HybridStrategy


# ------------------------------------------------------------
# 策略注册表（统一提供给 runner 使用）
# ------------------------------------------------------------
STRATEGY_REGISTRY = {
    "rr": RoundRobinStrategy,
    "sjf": ShortestJobFirstStrategy,
    "hrrn": HighestResponseRatioNextStrategy,
    "edf": EarliestDeadlineFirstStrategy,
    "hybrid": HybridStrategy,
}


__all__ = [
    "RoundRobinStrategy",
    "ShortestJobFirstStrategy",
    "HighestResponseRatioNextStrategy",
    "EarliestDeadlineFirstStrategy",
    "HybridStrategy",
    "STRATEGY_REGISTRY",
]

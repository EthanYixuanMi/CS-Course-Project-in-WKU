from __future__ import annotations

import argparse
import csv
import time
import json
import uuid
from pathlib import Path
from typing import List

from hybrid_scheduler.utils.models import Task
from hybrid_scheduler.strategies import STRATEGY_REGISTRY


# --------------------------------------------------------------------------
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strategy",
        required=True,
        choices=list(STRATEGY_REGISTRY),
        help="Scheduling Algorithm Name (e.g., RR / SJF / HRRN / EDF / Hybrid)",
    )
    parser.add_argument(
        "--workload",
        required=True,
        help="JSON workload file path",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Result CSV Path",
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Perform scheduling and metric calculations only; do not simulate time.sleep().",
    )
    return parser.parse_args()


# --------------------------------------------------------------------------
def _resolve_workload_path(path_str: str) -> Path:

    p = Path(path_str)

    # 1) Can you find it just by looking at the path provided by the user?
    if p.is_file():
        return p

    # 2) Try relative to the directory where this file is located: workloads/
    here = Path(__file__).resolve().parent  # .../hybrid_scheduler/experiments
    candidate = here / "workloads" / p.name
    if candidate.is_file():
        return candidate

    # If none are found, throw an error and indicate the paths that have been tried.
    raise FileNotFoundError(
        f"Cannot find workload file. Tried:\n" f"  - {p}\n" f"  - {candidate}"
    )


# --------------------------------------------------------------------------
def _load_tasks(path_str: str) -> List[Task]:

    path = _resolve_workload_path(path_str)

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    tasks: List[Task] = []

    for i, meta in enumerate(raw):
        # Ensure we do not directly modify the original dictionary.
        base = dict(meta)

        duration = float(base["duration"])
        category = base.get(
            "category", "CPU"
        )  # Can be converted from Pydantic to Category enumeration
        arrival = base.get("arrival", float(i))
        deadline = base.get("deadline")

        t = Task(
            id=str(uuid.uuid4()),
            category=category,
            duration=duration,
            arrival=arrival,
            deadline=deadline,
            meta=base,
        )
        tasks.append(t)

    return tasks


# --------------------------------------------------------------------------
def run_experiment(tasks: List[Task], strategy_name: str, dry: bool) -> List[Task]:

    cls = STRATEGY_REGISTRY[strategy_name]
    strategy = cls()

    # Scheduling and Sorting (The policy only concerns queue -> ordered queue)）
    ordered: List[Task] = strategy.schedule(tasks)

    # Logical Time Simulation
    current_time = 0.0
    for t in ordered:
        arrival = t.arrival if t.arrival is not None else 0.0

        start_time = max(current_time, arrival)
        t.wait_time = start_time - arrival

        finish_time = start_time + t.duration
        t.turnaround = finish_time - arrival

        current_time = finish_time

        if not dry:
            # For approximate simulation of "visual appearance" only; does not affect computational metrics.
            time.sleep(t.duration)

    return ordered


# --------------------------------------------------------------------------
def write_csv(tasks: List[Task], path: str) -> None:
    """
    Write the experimental results to CSV:

        id, category, wait_time, turnaround, duration
    """
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "category", "wait_time", "turnaround", "duration"])
        for t in tasks:
            w.writerow(
                [
                    t.id,
                    (
                        t.category.value
                        if hasattr(t.category, "value")
                        else str(t.category)
                    ),
                    t.wait_time,
                    t.turnaround,
                    t.duration,
                ]
            )


# --------------------------------------------------------------------------
def main() -> None:
    args = _parse_args()
    tasks = _load_tasks(args.workload)
    result = run_experiment(tasks, args.strategy, args.dry)
    write_csv(result, args.output)


if __name__ == "__main__":
    main()

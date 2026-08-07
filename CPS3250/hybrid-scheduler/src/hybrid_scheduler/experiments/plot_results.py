from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results",
        help="Directory for storing CSV result files (default: results)",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="peak_",
        help="Result file prefix (default: peak_, matches files like peak_rr.csv)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results/plots",
        help="Directory for output images (default: results/plots)",
    )
    return parser.parse_args()


def load_summaries(results_dir: Path, prefix: str) -> pd.DataFrame:
    """Read CSV files starting with the prefix in the specified directory and consolidate them into a single table."""
    rows = []

    for csv_path in sorted(results_dir.glob(f"{prefix}*.csv")):
        # File names follow the format: peak_rr.csv -> Strategy name is rr
        name = csv_path.stem  # peak_rr
        parts = name.split("_", 1)
        if len(parts) == 2:
            _, strategy = parts
        else:
            # If there is no underscore, treat the entire string as the policy name.
            strategy = name

        df = pd.read_csv(csv_path)

        # Calculate Average Wait Time & Turnaround Time
        wait_mean = df["wait_time"].mean()
        tat_mean = df["turnaround"].mean()

        rows.append(
            {
                "strategy": strategy,
                "file": csv_path.name,
                "wait_mean": wait_mean,
                "turnaround_mean": tat_mean,
            }
        )

    if not rows:
        raise RuntimeError(
            f"No CSV file with the prefix {prefix} was found in {results_dir}."
        )

    return pd.DataFrame(rows)


def plot_bar(df: pd.DataFrame, output_dir: Path, prefix: str) -> None:
    """Plot a bar chart comparing the average wait time and average turnaround time for each strategy."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sort by strategy name for easier reading
    df = df.sort_values("strategy")

    # 1) Average waiting time
    plt.figure()
    plt.bar(df["strategy"], df["wait_mean"])
    plt.xlabel("Strategy")
    plt.ylabel("Average Wait Time")
    plt.title(f"Average Wait Time per Strategy ({prefix.rstrip('_')})")
    plt.tight_layout()
    wait_path = output_dir / f"{prefix.rstrip('_')}_wait_time.png"
    plt.savefig(wait_path)

    # 2) Average Turnaround Time
    plt.figure()
    plt.bar(df["strategy"], df["turnaround_mean"])
    plt.xlabel("Strategy")
    plt.ylabel("Average Turnaround Time")
    plt.title(f"Average Turnaround Time per Strategy ({prefix.rstrip('_')})")
    plt.tight_layout()
    tat_path = output_dir / f"{prefix.rstrip('_')}_turnaround_time.png"
    plt.savefig(tat_path)


def main() -> None:
    args = _parse_args()

    results_dir = Path(args.results_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    summaries = load_summaries(results_dir, args.prefix)
    plot_bar(summaries, output_dir, args.prefix)


if __name__ == "__main__":
    main()

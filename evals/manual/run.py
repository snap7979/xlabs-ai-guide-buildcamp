"""
Run XLabs AI Guide on evaluation scenarios.

Usage:
    uv run python -m evals.manual.run --limit 1
    uv run python -m evals.manual.run
"""

import argparse
import csv
import json
import time
from pathlib import Path

from agent import agent


DATA_DIR = Path("evals/manual/data")


def run_agent_on_question(row):
    """Run one evaluation scenario."""
    history = []

    start = time.perf_counter()

    answer = agent(
        row["question"],
        tool_call_history=history,
    )

    elapsed = time.perf_counter() - start

    return {
        "input": row,
        "rag_response": {"answer": answer},
        "tools": history,
        "elapsed_seconds": round(elapsed, 2),
    }


def run_agent_on_all_questions(rows):
    """Run every selected scenario."""
    results = []

    for index, row in enumerate(rows, start=1):
        print(f"\n[{index}/{len(rows)}] {row['question']}")

        try:
            result = run_agent_on_question(row)
            results.append(result)
            print(f"Completed in {result['elapsed_seconds']}s")

        except Exception as exc:
            print(f"ERROR: {exc}")
            results.append({
                "input": row,
                "rag_response": {"answer": ""},
                "tools": [],
                "error": str(exc),
            })

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    with open(DATA_DIR / "scenarios.csv", newline="") as file:
        rows = list(csv.DictReader(file))

    if args.limit is not None:
        rows = rows[:args.limit]

    results = run_agent_on_all_questions(rows)

    output_path = DATA_DIR / "results.json"

    with open(output_path, "w") as file:
        json.dump(results, file, indent=2)

    print(f"\nSaved {len(results)} results to {output_path}")


if __name__ == "__main__":
    main()

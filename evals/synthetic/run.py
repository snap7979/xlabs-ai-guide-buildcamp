"""Run the agent against the generated synthetic evaluation cases."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from agent import MODEL, agent


DATA_DIR = Path(__file__).resolve().parent / "data"
INPUT_PATH = DATA_DIR / "generated_cases.json"
AGENT_PATH = Path(__file__).resolve().parents[2] / "agent.py"
OUTPUT_PATH = DATA_DIR / "agent_results_current_baseline.json"


def build_case_input(case):
    return (
        "Scenario facts (context only; do not treat as learner evidence):\n"
        f"{case['scenario']}\n\n"
        "Learner answer (assess this answer):\n"
        f"{case['learner_answer']}"
    )


def build_run_metadata(agent_path=AGENT_PATH, run_timestamp=None):
    if run_timestamp is None:
        run_timestamp = datetime.now(timezone.utc).isoformat()
    return {
        "model": MODEL,
        "agent_sha256": hashlib.sha256(agent_path.read_bytes()).hexdigest(),
        "run_timestamp": run_timestamp,
    }


def run_case(case, metadata, agent_function=agent):
    question = build_case_input(case)
    tool_call_history = []
    record = {
        "case_id": case["case_id"],
        "input": question,
        "agent_response": None,
        "tool_call_history": tool_call_history,
        "read_doc_requested_ids": [],
        **metadata,
    }
    try:
        record["agent_response"] = agent_function(
            question,
            tool_call_history=tool_call_history,
        )
    except Exception as error:
        record["error"] = {
            "type": type(error).__name__,
            "message": str(error),
        }
    else:
        record["error"] = None

    record["read_doc_requested_ids"] = [
        call["arguments"]["doc_id"]
        for call in tool_call_history
        if call["name"] == "read_doc"
        and isinstance(call.get("arguments"), dict)
        and isinstance(call["arguments"].get("doc_id"), str)
    ]
    return record


def write_results(results, output_path):
    with output_path.open("x", encoding="utf-8") as output_file:
        json.dump(results, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Run the six synthetic assessment cases."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="New baseline JSON path; existing files are never overwritten.",
    )
    args = parser.parse_args()
    output_path = args.output
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path
    if output_path.exists():
        raise FileExistsError(
            f"{output_path} already exists; refusing to overwrite results."
        )

    with INPUT_PATH.open(encoding="utf-8") as input_file:
        cases = json.load(input_file)
    if not isinstance(cases, list) or len(cases) != 6:
        raise ValueError(f"Expected six generated cases, got {len(cases)}")

    metadata = build_run_metadata()
    results = []
    successes = 0
    for index, case in enumerate(cases, start=1):
        print(f"\n[{index}/{len(cases)}] {case['case_id']}")
        result = run_case(case, metadata)
        results.append(result)
        if result["error"] is None:
            successes += 1
            print("Succeeded")
        else:
            print(
                f"FAILED: {result['error']['type']}: "
                f"{result['error']['message']}"
            )

    write_results(results, output_path)
    failures = len(results) - successes
    print(f"\nSuccesses: {successes}")
    print(f"Failures: {failures}")
    print(f"Output: {output_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify human Ground Truth labels against saved local evaluation evidence."""

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LABEL_FILE = Path("evals/ground_truth/data/human_review_labels.json")
CASE_FILE = Path("evals/ground_truth/data/reviewed_cases.json")
MANUAL_CASES = {"manual-scenarios-row-30", "manual-scenarios-row-31",
                "manual-scenarios-row-33", "manual-scenarios-row-36"}
EXPECTED_LABELS = {
    "debug-running-pods-2": "Good",
    "debug-services-2": "Bad",
    "dns-services-pods-2": "Bad",
    "debug-running-pods-1": "Good",
    "manual-scenarios-row-33": "Good",
    "debug-services-1": "Bad",
    "manual-scenarios-row-30": "Bad",
    "manual-scenarios-row-31": "Good",
    "manual-scenarios-row-36": "Good",
    "dns-services-pods-1": "Good",
}
EXPLICIT_OWNER_RATIONALES = {
    "debug-services-2": (
        "Agent failed to identify the learner's explicit misconception about "
        "ignoring Service selectors and labels."
    ),
    "dns-services-pods-2": (
        "Agent over-credited an unverified DNS diagnosis and did not explain "
        "the scope of Kubernetes Service-name resolution."
    ),
    "debug-services-1": (
        "Agent failed to credit the learner's port comparison and direct "
        "Pod-IP test, and redirected troubleshooting toward DNS without "
        "sufficient evidence."
    ),
    "manual-scenarios-row-30": (
        "Agent credited the learner with identifying missing endpoints, "
        "although that information appeared only in the scenario."
    ),
}
ORIGINAL_DATASET_SHA256 = {
    "evals/ground_truth/data/reviewed_cases.json":
        "5e3d84aa4ee5e85ab9373261ffd2d7e781b4b745e8e6fa1d3218712cf9993555",
    "data/kubernetes_troubleshooting_docs.json":
        "be1c9494f62c46714bbd7f8ec6b3a20b52637dd3a5078987024573c14b55796c",
    "evals/synthetic/data/generated_cases.json":
        "7e7aceff64812f93b04dd26f796379b2c62f1d281a56c8ae5711785001b40c8d",
    "evals/synthetic/data/agent_results_current_baseline.json":
        "611db98f78f8598a30f377fe61ce3a9653a2b6afbdbe109e2bfbb1bf6a5ef855",
    "evals/synthetic/data/agent_results.json":
        "bc4b1b4ba85f0324de580af8db3109412914cc6ebfac00ebe661fe9a1e2166f6",
    "evals/manual/data/scenarios.csv":
        "79b06407e59a5fb99fc286ad9ed9a63a02969fa2aa8b8c7a8ce3d9b25016e6ce",
    "evals/manual/data/results.json":
        "3ae0d304048da1b5bd2621bdc1a472b133a26cb0dbce9484a0a74cac9893d431",
    "evals/manual/data/results_labeled.json":
        "244c4f826600d6d27a906e7433b979d0b39303a3133079fbd36fc7355207635b",
}


def read_json(path: Path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify_original_datasets() -> None:
    for relative_path, expected_hash in ORIGINAL_DATASET_SHA256.items():
        path = ROOT / relative_path
        require(path.is_file(), f"Original dataset missing: {relative_path}")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        require(
            actual_hash == expected_hash,
            f"Original dataset changed: {relative_path} "
            f"(expected {expected_hash}, got {actual_hash})",
        )
    print(
        "[PASS] Original case/source/result datasets and existing manual "
        f"labels unchanged ({len(ORIGINAL_DATASET_SHA256)} SHA-256 pins)."
    )


def verify_manual_case(case: dict, label: dict, response: str) -> None:
    case_id = case["case_id"]
    input_ref = label["original_case_input_reference"]
    response_ref = label["saved_agent_response_reference"]
    row_number = input_ref["lookup"]["value"]
    record_number = response_ref["lookup"]["value"]

    require(
        input_ref["source_file"] == "evals/manual/data/scenarios.csv",
        f"{case_id}: unexpected manual scenario source",
    )
    require(
        case["input_origin"]["source_file"] == input_ref["source_file"] and
        case["input_origin"]["source_id"] == f"1-based row {row_number}",
        f"{case_id}: manual source row reference mismatch",
    )
    require(
        response_ref["source_file"] == "evals/manual/data/results.json",
        f"{case_id}: unexpected manual response source",
    )
    require(row_number == record_number, f"{case_id}: row/record mismatch")
    require(
        row_number == case["saved_agent_response"]["record_index_1based"],
        f"{case_id}: response record differs from reviewed-case reference",
    )

    scenarios_path = ROOT / input_ref["source_file"]
    with scenarios_path.open(encoding="utf-8", newline="") as file:
        scenario_rows = list(csv.DictReader(file))
    require(1 <= row_number <= len(scenario_rows), f"{case_id}: invalid CSV row")
    source_question = scenario_rows[row_number - 1]["question"]
    require(
        source_question == case["original_prompt"] == input_ref["question"],
        f"{case_id}: original question does not match CSV row {row_number}",
    )

    results = read_json(ROOT / response_ref["source_file"])
    require(1 <= record_number <= len(results), f"{case_id}: invalid result index")
    record = results[record_number - 1]
    require(
        record["input"]["question"] == source_question,
        f"{case_id}: saved manual response input mismatch",
    )
    require(
        response_ref["input_field"] == "input.question" and
        response_ref["input_value"] == source_question,
        f"{case_id}: recorded manual response input reference mismatch",
    )
    require(
        isinstance(response, str) and response,
        f"{case_id}: saved manual response text missing",
    )

    labeled_file = case["saved_agent_response"].get("identical_response_also_in")
    if labeled_file:
        labeled_results = read_json(ROOT / labeled_file)
        require(
            labeled_results[record_number - 1]["rag_response"] ==
            record["rag_response"],
            f"{case_id}: response differs from referenced labeled snapshot",
        )


def verify_synthetic_case(case: dict, label: dict, response: str) -> None:
    case_id = case["case_id"]
    source_ref = label["original_case_input_reference"]
    response_ref = label["saved_agent_response_reference"]
    require(
        source_ref["source_file"] == "evals/synthetic/data/generated_cases.json",
        f"{case_id}: unexpected synthetic case source",
    )
    require(
        response_ref["source_file"] ==
        "evals/synthetic/data/agent_results_current_baseline.json",
        f"{case_id}: unexpected synthetic response source",
    )
    require(
        source_ref["lookup"] == {
            "field": "case_id",
            "value": case["input_origin"]["source_id"],
        } and
        source_ref["lookup"]["value"] ==
        response_ref["lookup"]["value"] == case_id,
        f"{case_id}: synthetic case lookup mismatch",
    )

    generated_cases = read_json(ROOT / source_ref["source_file"])
    generated = [
        row for row in generated_cases if row["case_id"] == case_id
    ]
    require(len(generated) == 1, f"{case_id}: generated case not unique")
    generated = generated[0]
    require(
        generated["scenario"] == case["original_scenario"] and
        generated["learner_answer"] == case["learner_input"],
        f"{case_id}: original synthetic input mismatch",
    )
    require(
        generated["source_doc_id"] == case["repository_documentation"]["source_id"],
        f"{case_id}: source-document mapping mismatch",
    )

    response_rows = read_json(ROOT / response_ref["source_file"])
    records = [
        row for row in response_rows if row["case_id"] == case_id
    ]
    require(len(records) == 1, f"{case_id}: saved response not unique")
    record = records[0]
    expected_input = (
        "Scenario facts (context only; do not treat as learner evidence):\n"
        f"{case['original_scenario']}\n\n"
        "Learner answer (assess this answer):\n"
        f"{case['learner_input']}"
    )
    require(record["input"] == expected_input, f"{case_id}: saved input mismatch")
    require(
        record["error"] == case["saved_agent_response"]["error"],
        f"{case_id}: saved response error metadata mismatch",
    )
    require(
        isinstance(response, str) and response,
        f"{case_id}: saved synthetic response text missing",
    )


def main() -> int:
    labels = read_json(ROOT / LABEL_FILE)
    reviewed = read_json(ROOT / CASE_FILE)
    reviewed_by_id = {case["case_id"]: case for case in reviewed["cases"]}
    cases = labels["cases"]
    ids = [case["case_id"] for case in cases]
    expected_ids = list(EXPECTED_LABELS)

    require(len(ids) == 10, f"Expected 10 labels, found {len(ids)}")
    require(len(set(ids)) == 10, "Duplicate case IDs in human labels")
    require(ids == expected_ids, "Human label case order or IDs differ")
    require(len(reviewed_by_id) == 10, "Expected 10 unique reviewed case IDs")
    require(set(ids) == set(reviewed_by_id), "Reviewed case IDs differ")
    require(
        labels["review_date"] == "2026-11-08" and
        labels["review_method"] == "Human decision after AI-assisted review",
        "Review provenance metadata mismatch",
    )
    print("[PASS] Exactly 10 unique case IDs in required order.")

    counts = {"Good": 0, "Bad": 0}
    for case_label in cases:
        case_id = case_label["case_id"]
        reviewed_case = reviewed_by_id[case_id]
        require(
            case_label["human_label"] == EXPECTED_LABELS[case_id],
            f"{case_id}: unexpected final label",
        )
        require(
            case_label["review_date"] == labels["review_date"] and
            case_label["review_method"] == labels["review_method"],
            f"{case_id}: review metadata mismatch",
        )
        counts[case_label["human_label"]] += 1
        require(
            case_label["ground_truth_case_reference"]["source_file"] ==
            "evals/ground_truth/data/reviewed_cases.json" and
            case_label["ground_truth_case_reference"]["lookup"] ==
            {"field": "case_id", "value": case_id},
            f"{case_id}: Ground Truth reference mismatch",
        )

        human_rationale = case_label.get("explicit_human_rationale")
        if case_id in EXPLICIT_OWNER_RATIONALES:
            require(
                human_rationale == EXPLICIT_OWNER_RATIONALES[case_id],
                f"{case_id}: explicit owner rationale mismatch",
            )
        else:
            require(
                human_rationale is None,
                f"{case_id}: unsupported human rationale attribution",
            )

        initial = case_label["initial_copilot_provisional_recommendation"]
        require(initial in {"Good", "Bad"}, f"{case_id}: invalid provisional label")
        response_ref = case_label["saved_agent_response_reference"]
        reviewed_response_ref = reviewed_case["saved_agent_response"]
        require(
            response_ref["source_file"] == reviewed_response_ref["source_file"],
            f"{case_id}: saved response source differs from reviewed dataset",
        )
        require(
            response_ref["response_sha256"] ==
            reviewed_response_ref["response_sha256"],
            f"{case_id}: recorded response hashes differ",
        )

        if case_id in MANUAL_CASES:
            response_rows = read_json(ROOT / response_ref["source_file"])
            index = response_ref["lookup"]["value"]
            require(
                response_ref["lookup"] ==
                {"field": "record_index_1based", "value": index},
                f"{case_id}: invalid manual response lookup",
            )
            response_record = response_rows[index - 1]
            response = response_record["rag_response"]["answer"]
            verify_manual_case(reviewed_case, case_label, response)
        else:
            response_rows = read_json(ROOT / response_ref["source_file"])
            matching_records = [
                row for row in response_rows
                if row["case_id"] == response_ref["lookup"]["value"]
            ]
            require(
                len(matching_records) == 1,
                f"{case_id}: saved response lookup is not unique",
            )
            record = matching_records[0]
            response = record["agent_response"]
            verify_synthetic_case(reviewed_case, case_label, response)

        actual_hash = sha256_text(response)
        require(
            actual_hash == response_ref["response_sha256"],
            f"{case_id}: response SHA-256 mismatch "
            f"(expected {response_ref['response_sha256']}, got {actual_hash})",
        )

    require(counts == {"Good": 6, "Bad": 4}, f"Unexpected label totals: {counts}")
    print("[PASS] Exact final labels and totals: 6 Good, 4 Bad.")
    print("[PASS] All 10 Ground Truth references, input mappings, and response mappings resolve.")
    print("[PASS] All 10 saved response SHA-256 hashes match.")
    print("[PASS] Explicit rationale is limited to the four owner-provided cases.")
    verify_original_datasets()
    print("Human Ground Truth review verification: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Human Ground Truth review verification: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)


import asyncio
import json
from pathlib import Path

import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from evals.manual.judge import (
    create_log_judge_agent,
    format_judge_prompt,
)

DATA_DIR = Path("evals/manual/data")


async def evaluate_sample(judge, row):
    prompt = format_judge_prompt(row)
    result = await judge.run(prompt)
    return result.output


async def main():
    input_path = DATA_DIR / "results_labeled.json"
    output_path = DATA_DIR / "judge_evaluated.csv"

    with open(input_path, encoding="utf-8") as f:
        results = json.load(f)

    # Use only human-reviewed cases.
    reviewed = [
        row for row in results
        if row.get("label") in ("good", "bad")
    ]

    print(f"Human-reviewed cases: {len(reviewed)}")

    judge = create_log_judge_agent()
    rows = []

    for i, row in enumerate(reviewed, start=1):
        print(f"Evaluating {i}/{len(reviewed)}...")

        try:
            evaluation = await evaluate_sample(judge, row)
            llm_label = evaluation.label
            reasoning = evaluation.reasoning

        except Exception as e:
            print(f"Judge error on case {i}: {e}")
            llm_label = None
            reasoning = f"Evaluation failed: {e}"

        rows.append({
            "question": row["input"]["question"],
            "human_label": row["label"],
            "human_comment": row.get("comments", ""),
            "llm_label": llm_label,
            "llm_reasoning": reasoning,
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)

    # Exclude technical failures from judge metrics.
    valid = df[df["llm_label"].isin(["good", "bad"])]

    if valid.empty:
        print("No successful judge evaluations.")
        return

    y_true_bad = valid["human_label"] == "bad"
    y_pred_bad = valid["llm_label"] == "bad"

    tp = (y_true_bad & y_pred_bad).sum()
    fp = (~y_true_bad & y_pred_bad).sum()
    fn = (y_true_bad & ~y_pred_bad).sum()
    tn = (~y_true_bad & ~y_pred_bad).sum()

    accuracy = (tp + tn) / len(valid)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    print("\n--- Judge Evaluation Results ---")
    print(f"Evaluated: {len(valid)}")
    print(f"Failed: {len(df) - len(valid)}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Precision (bad): {precision:.3f}")
    print(f"Recall (bad): {recall:.3f}")

    print("\nConfusion Matrix:")
    print(f"TP={tp}, FP={fp}, FN={fn}, TN={tn}")

    disagreements = valid[
        valid["human_label"] != valid["llm_label"]
    ]

    print(f"\nDisagreements: {len(disagreements)}")

    for _, row in disagreements.iterrows():
        print(f"\nQuestion: {row['question']}")
        print(f"Human: {row['human_label']}")
        print(f"Judge: {row['llm_label']}")
        print(f"Reasoning: {row['llm_reasoning']}")

    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
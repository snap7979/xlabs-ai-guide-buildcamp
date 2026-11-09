import argparse
import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator


ROOT_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_PATH = ROOT_DIR / "data" / "kubernetes_troubleshooting_docs.json"
OUTPUT_PATH = ROOT_DIR / "evals" / "synthetic" / "data" / "generated_cases.json"
MODEL = "gpt-4o-mini"


class ReferenceAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    demonstrated_understanding: list[str]
    explicit_misconceptions: list[str]
    checks_not_discussed: list[str]
    suggested_next_steps: list[str] = Field(min_length=1)


class GeneratedCaseContent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario: str = Field(min_length=1)
    learner_answer: str = Field(min_length=1)
    reference_assessment: ReferenceAssessment


class GeneratedCases(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cases: list[GeneratedCaseContent] = Field(min_length=2, max_length=2)

    @model_validator(mode="after")
    def contains_correct_and_misconception_cases(self):
        misconception_counts = [
            bool(case.reference_assessment.explicit_misconceptions)
            for case in self.cases
        ]
        if misconception_counts.count(True) != 1:
            raise ValueError(
                "Expected one correct-reasoning case and one explicit "
                "misconception case"
            )
        return self


def load_documents():
    documents = json.loads(DOCUMENTS_PATH.read_text(encoding="utf-8"))
    if not isinstance(documents, list) or len(documents) != 3:
        raise ValueError("Expected exactly three Kubernetes documentation records")

    required = ("doc_id", "title", "symptoms", "guidance", "commands", "source_url")
    doc_ids = set()
    for document in documents:
        if not isinstance(document, dict) or any(
            not document.get(field) for field in required
        ):
            raise ValueError("Documentation record is missing required fields")
        if document["doc_id"] in doc_ids:
            raise ValueError(f"Duplicate documentation ID: {document['doc_id']}")
        doc_ids.add(document["doc_id"])

    return documents


def generate_for_document(client, document):
    response = client.responses.create(
        model=MODEL,
        instructions=(
            "Create exactly two evaluation cases for an AI agent that assesses "
            "a learner's Kubernetes troubleshooting reasoning, not a generic "
            "question-answering chatbot. The first case must show correct "
            "reasoning with no explicit misconception. The second must contain "
            "one explicit technical misconception. For each, provide a "
            "realistic troubleshooting scenario and learner answer, then a "
            "reference assessment with demonstrated understanding, explicit "
            "misconceptions (empty when none), checks not discussed, and "
            "suggested next steps. Every demonstrated-understanding or "
            "misconception item must be directly supported by explicit evidence "
            "in the learner answer; never infer or invent either from silence, "
            "scenario context, or likely learner intent. Use an empty "
            "demonstrated_understanding list when no understanding is evidenced "
            "and an empty checks_not_discussed list when no documented, relevant "
            "check is clearly omitted from the learner answer. Ground every "
            "assessment only in the supplied documentation record. Do not "
            "invent commands, behavior, or URLs. "
            "Do not include source document IDs or URLs; those are added from "
            "the verified source record."
        ),
        input=json.dumps(document, ensure_ascii=False),
        text={
            "format": {
                "type": "json_schema",
                "name": "synthetic_evaluation_cases",
                "strict": True,
                "schema": GeneratedCases.model_json_schema(),
            }
        },
    )
    return GeneratedCases.model_validate_json(response.output_text)


def validate_cases(cases, documents):
    source_by_id = {document["doc_id"]: document for document in documents}
    if len(cases) != 6:
        raise ValueError(f"Expected six generated cases, got {len(cases)}")

    seen_case_ids = set()
    counts_by_document = {doc_id: 0 for doc_id in source_by_id}
    for case in cases:
        if case["source_doc_id"] not in source_by_id:
            raise ValueError(f"Unknown source document ID: {case['source_doc_id']}")
        source = source_by_id[case["source_doc_id"]]
        if case["source_url"] != source["source_url"]:
            raise ValueError(f"Unexpected source URL for {case['source_doc_id']}")
        if case["case_id"] in seen_case_ids:
            raise ValueError(f"Duplicate case ID: {case['case_id']}")
        seen_case_ids.add(case["case_id"])
        counts_by_document[case["source_doc_id"]] += 1

    if any(count != 2 for count in counts_by_document.values()):
        raise ValueError("Expected exactly two cases per source document")


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic evaluations.")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Call OpenAI to generate cases and save the dataset.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing generated_cases.json (requires --generate).",
    )
    args = parser.parse_args()

    if args.overwrite and not args.generate:
        parser.error("--overwrite requires --generate")

    try:
        documents = load_documents()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(f"Cannot load documentation records: {error}")

    if not args.generate:
        print("Dry run: no OpenAI requests made.")
        print(f"Loaded {len(documents)} documentation records.")
        print("Planned cases: 2 per document, 6 total.")
        for document in documents:
            print(
                f"- {document['doc_id']}: "
                "1 correct-reasoning case, 1 explicit-misconception case"
            )
        print(f"Output would be: {OUTPUT_PATH}")
        print("Generated references are provisional until manually reviewed.")
        return

    if OUTPUT_PATH.exists() and not args.overwrite:
        parser.error(
            f"{OUTPUT_PATH} already exists; pass --overwrite to replace it."
        )

    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(ROOT_DIR / ".env")
    client = OpenAI()
    cases = []
    for document in documents:
        generated = generate_for_document(client, document)
        for index, content in enumerate(generated.cases, start=1):
            case = content.model_dump()
            case.update(
                {
                    "case_id": f"{document['doc_id']}-{index}",
                    "source_doc_id": document["doc_id"],
                    "source_url": document["source_url"],
                }
            )
            cases.append(case)

    validate_cases(cases, documents)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if args.overwrite else "x"
    with OUTPUT_PATH.open(mode, encoding="utf-8") as output_file:
        json.dump(cases, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    print(f"Saved {len(cases)} provisional cases to {OUTPUT_PATH}")
    print("Review all generated references manually before using them.")


if __name__ == "__main__":
    main()

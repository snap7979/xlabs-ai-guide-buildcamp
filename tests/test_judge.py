import json

from dotenv import load_dotenv
from openai import OpenAI

from agent import MODEL, agent
from tools import get_scenario


def assert_criteria(response, criteria):
    load_dotenv()
    client = OpenAI()
    schema = {
        "type": "object",
        "properties": {
            "passed": {"type": "boolean"},
            "reason": {"type": "string"},
        },
        "required": ["passed", "reason"],
        "additionalProperties": False,
    }

    for name, criterion in criteria:
        evaluation = client.responses.create(
            model=MODEL,
            instructions=(
                "You are an impartial evaluator. Judge only the supplied "
                "criterion against the reference and response. Return a "
                "pass only when the response clearly satisfies the criterion."
            ),
            input=(
                f"Criterion ({name}): {criterion}\n\n"
                f"Response to evaluate:\n{response}"
            ),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "criteria_evaluation",
                    "strict": True,
                    "schema": schema,
                }
            },
        )
        result = json.loads(evaluation.output_text)
        assert result["passed"], f"{name}: {result['reason']}"


def test_agent_response_passes_llm_judge():
    scenario = get_scenario("services-networking")
    answer = agent(
        "Retrieve the saved Kubernetes scenario services-networking. "
        "Provide its title and scenario text without solving it."
    )

    criteria = [
        (
            "Correctness",
            "The response accurately reproduces the saved scenario title "
            f"{scenario['title']!r} and its meaning: {scenario['scenario']!r}.",
        ),
        (
            "Relevance",
            "The response provides the requested saved scenario without "
            "solving it or adding unrelated troubleshooting advice.",
        ),
    ]

    assert_criteria(answer, criteria)

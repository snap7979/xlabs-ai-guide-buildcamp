import json
from pathlib import Path
from types import SimpleNamespace

import agent as agent_module


CASES_PATH = (
    Path(__file__).resolve().parents[1]
    / "evals"
    / "synthetic"
    / "data"
    / "generated_cases.json"
)


class FakeResponses:
    def __init__(self):
        self.request = None

    def create(self, **request):
        self.request = request
        return SimpleNamespace(output=[], output_text="offline response")


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_debug_services_assessment_prompt_separates_scenario_and_evidence():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    case = next(case for case in cases if case["case_id"] == "debug-services-2")
    question = (
        "Scenario facts (context only; do not treat as learner evidence):\n"
        f"{case['scenario']}\n\n"
        "Learner answer (assess this answer):\n"
        f"{case['learner_answer']}"
    )
    client = FakeClient()

    answer = agent_module._run_agent(question, openai_client=client)

    request = client.responses.request
    instructions = " ".join(request["instructions"].split())
    assert answer == "offline response"
    assert request["input"] == question
    assert "Scenario facts (context only; do not treat as learner evidence):" in question
    assert "Learner answer (assess this answer):" in question
    assert (
        "For every demonstrated-understanding claim, identify specific words "
        "or a close paraphrase from the learner's response that support it."
        in instructions
    )
    assert (
        "If the learner explicitly states or reasons from a fact also present "
        "in the scenario, credit only the reasoning they actually express"
        in instructions
    )
    assert (
        "Credit an explicitly stated, technically reasonable diagnostic "
        "hypothesis as a possibility, not as a verified finding."
        in instructions
    )
    assert (
        "Describe a diagnosis as confirmed only when the learner provides "
        "supporting evidence; do not treat uncertainty alone as a misconception."
        in instructions
    )
    assert (
        "A relevant check never mentioned by the learner may be classified "
        "as not discussed. If the learner explicitly mentions but chooses to "
        "skip a check, describe it as mentioned but skipped, not as not "
        "mentioned."
        in instructions
    )
    assert (
        "A misconception requires an explicitly stated, technically "
        "incorrect belief. Deliberately skipping a useful check does not "
        "by itself prove a misconception."
        in instructions
    )
    assert (
        "output a shell command unless its complete text exactly matches a "
        "complete command line in the commands field of a retrieved document. "
        "Treat those command lines as a literal allowlist."
        in instructions
    )
    assert (
        "Do not combine commands, substitute arguments, or construct a new "
        "command from documentation guidance."
        in instructions
    )
    assert (
        "When the documentation supports a diagnostic step but provides no "
        "allowed command, describe the step in plain language without a "
        "shell command."
        in instructions
    )

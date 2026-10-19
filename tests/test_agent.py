from agent import agent
from tools import get_scenario


def test_agent_retrieves_saved_scenario():
    scenario_id = "services-networking"
    expected_scenario = get_scenario(scenario_id)
    tool_call_history = []

    answer = agent(
        f"Retrieve the saved Kubernetes scenario {scenario_id}. "
        "Return its title and scenario text verbatim.",
        tool_call_history=tool_call_history,
    )

    assert {
        "name": "get_scenario",
        "arguments": {"scenario_id": scenario_id},
    } in tool_call_history
    assert expected_scenario["title"] in answer
    assert expected_scenario["scenario"] in answer

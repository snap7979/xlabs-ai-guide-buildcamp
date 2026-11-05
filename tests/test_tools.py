from tools import get_scenario


def test_get_scenario_returns_known_scenario():
    assert get_scenario("services-networking") == {
        "scenario_id": "services-networking",
        "domain": "kubernetes",
        "title": "Services and networking",
        "scenario": (
            "A Kubernetes Service exists, but requests do not reach its Pods. "
            "What would you inspect first, and what evidence would distinguish "
            "a selector or endpoint problem from a wider network problem?"
        ),
    }

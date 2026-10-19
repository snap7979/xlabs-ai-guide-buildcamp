import json
from pathlib import Path

from minsearch import Index


DATA_DIR = Path(__file__).resolve().parent / "data"
DOCUMENTS_PATH = DATA_DIR / "kubernetes_troubleshooting_docs.json"
SCENARIOS_PATH = DATA_DIR / "kubernetes_scenarios.json"

documents = json.loads(DOCUMENTS_PATH.read_text(encoding="utf-8"))

index = Index(
    text_fields=["title", "symptoms", "guidance", "commands", "source_title"],
    keyword_fields=["doc_id", "category"],
)
index.fit(documents)


def search_docs(query):
    results = index.search(query, num_results=5)

    return [
        {
            "doc_id": doc["doc_id"],
            "title": doc["title"],
            "snippet": doc["symptoms"],
            "source_url": doc["source_url"],
        }
        for doc in results
    ]


def read_doc(doc_id):
    for doc in documents:
        if doc["doc_id"] == doc_id:
            return doc

    return {"error": f"Document not found: {doc_id}"}


def get_scenario(scenario_id):
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))

    for scenario in scenarios:
        if scenario["scenario_id"] == scenario_id:
            return scenario

    return {"error": f"Scenario not found: {scenario_id}"}


tools = [
    {
        "type": "function",
        "name": "search_docs",
        "description": "Search local Kubernetes troubleshooting notes and return brief results with document IDs and source URLs.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_doc",
        "description": "Read the full locally stored Kubernetes troubleshooting document by its document ID.",
        "parameters": {
            "type": "object",
            "properties": {"doc_id": {"type": "string"}},
            "required": ["doc_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_scenario",
        "description": "Retrieve a saved Kubernetes troubleshooting scenario by its scenario ID.",
        "parameters": {
            "type": "object",
            "properties": {"scenario_id": {"type": "string"}},
            "required": ["scenario_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def execute_tool(name, arguments):
    if name == "search_docs":
        return search_docs(arguments["query"])

    if name == "read_doc":
        return read_doc(arguments["doc_id"])

    if name == "get_scenario":
        return get_scenario(arguments["scenario_id"])

    return {"error": f"Unknown tool: {name}"}

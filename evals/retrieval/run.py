import json
from pathlib import Path

from tools import search_docs


QUERIES_PATH = Path(__file__).resolve().parent / "data" / "queries.json"


def main():
    queries = json.loads(QUERIES_PATH.read_text(encoding="utf-8"))
    top_one_count = 0

    for number, item in enumerate(queries, start=1):
        results = search_docs(item["query"])
        returned_doc_ids = [result["doc_id"] for result in results]
        expected_doc_id = item["expected_doc_id"]
        rank = (
            returned_doc_ids.index(expected_doc_id) + 1
            if expected_doc_id in returned_doc_ids
            else None
        )
        ranked_first = rank == 1
        top_one_count += ranked_first

        print(f"Query {number}: {item['query']}")
        print(f"  Returned document IDs: {returned_doc_ids}")
        print(f"  Expected document ID: {expected_doc_id}")
        print(f"  Expected document rank: {rank if rank is not None else 'not found'}")
        print(f"  Ranked first: {'yes' if ranked_first else 'no'}")

    total = len(queries)
    accuracy = top_one_count / total if total else 0
    print(f"\nTop-1 Accuracy: {top_one_count}/{total} ({accuracy:.1%})")


if __name__ == "__main__":
    main()

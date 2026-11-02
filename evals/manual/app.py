import json
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from tools import read_doc



DATA_DIR = Path(__file__).resolve().parent / "data"
SOURCE = DATA_DIR / "results.json"
LABELS = DATA_DIR / "results_labeled.json"

FAILURE_CATEGORIES = [
    "Unsupported claim",
    "Invented learner understanding",
    "Missed misconception",
    "Incorrect technical feedback",
    "Unhelpful next steps",
    "Instruction following",
    "Other",
]


def load_results():
    path = LABELS if LABELS.exists() else SOURCE
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data:
        item.setdefault("label", None)
        item.setdefault("comments", "")
        item.setdefault("failure_category", None)
    return data


def save_results(data):
    LABELS.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


st.set_page_config(page_title="XLabs Manual Evaluation", layout="wide")
st.title("XLabs AI Guide — Manual Evaluation")

if not SOURCE.exists():
    st.error("results.json not found.")
    st.stop()

if "eval_data" not in st.session_state:
    st.session_state.eval_data = load_results()

data = st.session_state.eval_data

labeled = sum(item["label"] in ("good", "bad") for item in data)
st.sidebar.metric("Reviewed", f"{labeled} / {len(data)}")
st.sidebar.progress(labeled / len(data))

if "pending_index" in st.session_state:
    st.session_state.selected_result = st.session_state.pop("pending_index")

index = st.sidebar.selectbox(
    "Select result",
    range(len(data)),
    format_func=lambda i: (
        f"{'✅' if data[i]['label'] == 'good' else '❌' if data[i]['label'] == 'bad' else '⬜'} "
        f"Run {i + 1}"
    ),
    key="selected_result",
)

item = data[index]
st.subheader(f"Run {index + 1} / {len(data)}")

st.caption(
    f"Group: {item['input'].get('group', 'N/A')} | "
    f"Type: {item['input'].get('type', 'N/A')}"
)

st.subheader("Question")
st.write(item["input"]["question"])

st.subheader("Agent Answer")
st.markdown(item.get("rag_response", {}).get("answer", ""))

with st.expander("Tool Calls"):
    st.json(item.get("tools", []))

with st.expander("Retrieved Documentation"):
    seen = set()
    found = False

    for tool in item.get("tools", []):
        if tool.get("name") != "read_doc":
            continue

        arguments = tool.get("arguments", {})
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                continue

        doc_id = arguments.get("doc_id")
        if not doc_id or doc_id in seen:
            continue

        seen.add(doc_id)
        found = True
        st.markdown(f"**Document: `{doc_id}`**")
        st.json(read_doc(doc_id))

    if not found:
        st.info("No read_doc calls recorded.")

st.divider()
st.subheader("Human Label")

with st.form(key=f"label_form_{index}"):
    current = item.get("label")
    choices = ["Not selected", "Good", "Bad"]
    selected = (
        1 if current == "good"
        else 2 if current == "bad"
        else 0
    )

    decision = st.radio(
        "Is the agent response good?",
        choices,
        index=selected,
    )

    category = st.selectbox(
        "Failure category (for Bad)",
        ["Not selected"] + FAILURE_CATEGORIES,
        index=(
            FAILURE_CATEGORIES.index(item["failure_category"]) + 1
            if item.get("failure_category") in FAILURE_CATEGORIES
            else 0
        ),
    )

    comments = st.text_area(
        "Evidence / Comments",
        value=item.get("comments", ""),
    )

    submitted = st.form_submit_button("Save Label & Next")

if submitted:
    if decision == "Not selected":
        st.warning("Select Good or Bad.")
    elif decision == "Bad" and category == "Not selected":
        st.warning("Select a failure category.")
    elif not comments.strip():
        st.warning("Add an evidence-based comment.")
    else:
        item["label"] = decision.lower()
        item["failure_category"] = (
            category if decision == "Bad" else None
        )
        item["comments"] = comments.strip()
        save_results(data)

        next_index = next(
            (
                i for i in range(index + 1, len(data))
                if data[i]["label"] is None
            ),
            None,
        )
        if next_index is None:
            next_index = next(
                (
                    i for i in range(len(data))
                    if data[i]["label"] is None
                ),
                index,
            )

        st.session_state.pending_index = next_index
        st.rerun()

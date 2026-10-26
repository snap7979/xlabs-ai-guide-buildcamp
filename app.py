import streamlit as st

from agent import agent


st.set_page_config(
    page_title="XLabs AI Guide",
    page_icon="🧭",
    layout="centered",
)

SCENARIOS = {
    "Service Connectivity": {
        "description": (
            "A Kubernetes Service cannot reach its Pods. "
            "Users cannot access the application through the Service."
        ),
        "question": (
            "How would you investigate this problem? "
            "Explain the diagnostic steps you would take and why."
        ),
    },
    "Pod Troubleshooting": {
        "description": (
            "A Kubernetes Pod is not running as expected. "
            "The application is unavailable."
        ),
        "question": (
            "How would you investigate the Pod's status "
            "and identify the cause of the problem?"
        ),
    },
    "DNS Resolution": {
        "description": (
            "A Pod can reach another Pod by IP address, "
            "but cannot resolve a Kubernetes Service name."
        ),
        "question": (
            "How would you troubleshoot DNS resolution "
            "inside the Kubernetes cluster?"
        ),
    },
}

st.title("🧭 XLabs AI Guide")
st.caption("Kubernetes Troubleshooting Assessment")

st.divider()

selected_scenario = st.selectbox(
    "Choose a troubleshooting scenario",
    options=list(SCENARIOS.keys()),
)

scenario = SCENARIOS[selected_scenario]

st.subheader(selected_scenario)

with st.container(border=True):
    st.markdown("**Scenario**")
    st.write(scenario["description"])

    st.markdown("**Your Challenge**")
    st.write(scenario["question"])

st.markdown("### Your Answer")

learner_answer = st.text_area(
    "Explain your troubleshooting approach",
    height=170,
    placeholder=(
        "Describe what you would check, "
        "which commands you might use, and why..."
    ),
    label_visibility="collapsed",
    key=f"answer_{selected_scenario}",
)

if st.button("Submit Assessment", type="primary"):
    if not learner_answer.strip():
        st.warning("Please write your answer before submitting.")
    else:
        question_for_agent = (
            f"Troubleshooting scenario:\n"
            f"{scenario['description']}\n\n"
            f"Question presented to the learner:\n"
            f"{scenario['question']}\n\n"
            f"Learner's response to evaluate:\n"
            f"{learner_answer.strip()}"
        )

        tool_history = []

        with st.spinner("Evaluating your understanding..."):
            assessment = agent(
                question_for_agent,
                tool_call_history=tool_history,
            )

        st.divider()
        st.subheader("Your Assessment")
        st.markdown(assessment)

        with st.expander("Technical Details — Tool Activity"):
            if tool_history:
                for step, tool in enumerate(tool_history, start=1):
                    st.write(f"{step}. {tool['name']}")
                    st.json(tool["arguments"])
            else:
                st.info("No tool calls recorded.")
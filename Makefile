.PHONY: help setup test-offline run

help:
	@printf '%s\n' \
		'help          Show available commands' \
		'setup         Install locked dependencies with uv' \
		'test-offline  Run the offline test suite' \
		'run           Start the Streamlit application'

setup:
	uv sync --frozen

test-offline:
	uv run --no-sync pytest -q tests/test_tools.py tests/test_agent_instructions.py

run:
	uv run streamlit run app.py

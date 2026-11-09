# Bonus Runtime Verification Evidence

## Verification context

- **Date:** 2026-11-08
- **Repository:** branch `feat/synthetic-evaluation`, commit
  `eedcfac1ace8dc52b4af6fd48dffde7cd57274c4`
- **Scope:** B5 Docker, B6 Docker Compose, B7 Makefile, and B10 local Agent UI.
- No Agent inference, LLM/Judge/API request, dependency installation, fresh
  Docker image build, or evaluation was performed as part of this verification.

## Evidence provenance

- **User-executed observations:** B5 and B6 terminal results and B10 browser
  rendering below were reported by the user as observed on November 8, 2026.
  The terminal output and browser screenshots are not saved in this repository;
  these results are documented as user-reported, not independently reproduced
  by Copilot.
- **Copilot-executed test:** B7 `make test-offline` was run directly during
  Step 24B and its command output was observed.
- **Historical claims:** Earlier Docker build, Compose, and three-scenario
  visual checks were reported as prior results. Where no execution transcript
  or screenshot is saved in the repository, those claims remain historical
  context rather than independently verifiable evidence.

## Results

| Bonus | Status | Evidence and provenance | Remaining limitation |
|---|---|---|---|
| **B5 Docker** | **PASS — runtime smoke test** | User-reported terminal observations: existing image `xlabs-ai-guide:step14` started successfully in a temporary container bound to localhost; root HTTP **200**; Streamlit health HTTP **200**, response `ok`; temporary container was subsequently removed. | No fresh image build was performed in this verification. The existing image's build provenance against the current workspace is not established. Terminal output is not saved in the repository. |
| **B6 Docker Compose** | **PASS — runtime verification** | User-reported terminal observations: `docker compose config --quiet` passed; service `app` ran in isolated project `xlabs-step24c-b6-20261108`; `docker compose ps` showed `Up`; root HTTP **200**; Streamlit health HTTP **200**, response `ok`; `docker compose down` removed the test container and network successfully. | Terminal output is not saved in the repository. |
| **B7 Makefile** | **PASS** | Copilot executed `make test-offline`; exit code **0**. It ran `uv run --no-sync pytest -q tests/test_tools.py tests/test_agent_instructions.py`; **2 passed in 15.76s**, no failures or errors. | This verifies the offline Make target, not external service integration. |
| **B10 Agent UI** | **PASS — Supported (provisional)** | The owner confirms the UI was previously inspected with three scenarios. The current review includes a browser screenshot of the running Streamlit app through Docker Compose showing the scenario selector, Service Connectivity scenario and challenge, learner answer input, and Submit Assessment button. The root and health HTTP endpoints both returned **200**. | No Agent/API submission was made during the current verification; end-to-end Agent inference was not newly tested. |

## B5 Docker — user-reported terminal observations

- Existing image: `xlabs-ai-guide:step14`.
- The temporary test container started successfully and was bound only to
  `127.0.0.1:18581`.
- Root endpoint: HTTP **200**.
- Streamlit health endpoint: HTTP **200**, body `ok`.
- The temporary test container was subsequently removed.
- **No fresh Docker build was performed** during this verification.
- The exact `docker run` invocation and raw terminal transcript are not saved
  in the repository; the results above are attributed to the user's report.

## B6 Docker Compose — user-reported terminal observations

Commands and observations reported:

```sh
docker compose config --quiet
docker compose ps
docker compose down
```

- Configuration validation passed.
- Service: `app`.
- Isolated project: `xlabs-step24c-b6-20261108`.
- The container started successfully; `docker compose ps` showed `Up`.
- Root endpoint: HTTP **200**.
- Streamlit health endpoint: HTTP **200**, body `ok`.
- `docker compose down` removed the temporary test container and network
  successfully.
- These are user-reported results; no raw terminal transcript is saved in the
  repository.

## B7 Makefile — Copilot-executed test

Executed:

```sh
make test-offline
```

Exit code **0**. Make invoked:

```sh
uv run --no-sync pytest -q tests/test_tools.py tests/test_agent_instructions.py
```

Result: **2 passed in 15.76s** (`.. [100%]`). No external API request was
made.

## B10 Agent UI — owner-confirmed history and current browser observation

The project owner confirms that the UI was previously tested with three
scenarios; this is owner-confirmed historical evidence. The current review
includes a browser screenshot showing the running Streamlit application
through Docker Compose, with the scenario selector, Service Connectivity
scenario and challenge, learner answer input, and Submit Assessment button.
The root and Streamlit health HTTP endpoints both returned **200**.

The current verification did not submit an Agent/API request. It therefore
does not establish that end-to-end Agent inference was newly tested. On the
available UI evidence, B10 is **PASS — Supported (provisional)**.

## Historical report reconciliation

- Earlier Docker image-build and Docker/Compose runtime results were
  historically reported. The B5/B6 observations in this report are additional
  user-reported terminal results; they do not establish that the existing
  image was freshly built from the current workspace.
- The Makefile test is independently verified by the Copilot-executed Step
  24B run recorded above.
- The three-scenario inspection is owner-confirmed historical evidence. The
  current browser screenshot directly verifies the rendered UI and listed
  controls, but does not demonstrate a current interactive selection across
  all three scenarios or an Agent/API assessment.
- The current review includes a browser screenshot, but it is not saved in the
  repository.

## Integrity and preserved data

The evaluation-file hashes were checked before and after this report update;
the values were unchanged:

- `evals/ground_truth/data/reviewed_cases.json`:
  `5e3d84aa4ee5e85ab9373261ffd2d7e781b4b745e8e6fa1d3218712cf9993555`
- `evals/ground_truth/data/human_review_labels.json`:
  `a9297becabbba184292edf4c66a21f4ebcf111d86c647090bb85237cd7e22615`
- `evals/synthetic/data/generated_cases.json`:
  `7e7aceff64812f93b04dd26f796379b2c62f1d281a56c8ae5711785001b40c8d`
- `evals/synthetic/data/agent_results_current_baseline.json`:
  `611db98f78f8598a30f377fe61ce3a9653a2b6afbdbe109e2bfbb1bf6a5ef855`
- `evals/synthetic/data/agent_results.json`:
  `bc4b1b4ba85f0324de580af8db3109412914cc6ebfac00ebe661fe9a1e2166f6`
- `evals/manual/data/scenarios.csv`:
  `79b06407e59a5fb99fc286ad9ed9a63a02969fa2aa8b8c7a8ce3d9b25016e6ce`
- `evals/manual/data/results.json`:
  `3ae0d304048da1b5bd2621bdc1a472b133a26cb0dbce9484a0a74cac9893d431`
- `evals/manual/data/results_labeled.json`:
  `244c4f826600d6d27a906e7433b979d0b39303a3133079fbd36fc7355207635b`
- `evals/manual/data/judge_evaluated.csv`:
  `9d84d48508f14dbdd6adf24de011015e1a9af73251eb1ac91de82b825e6082cb`

Only this runtime verification report was modified. No application source files,
human review labels, or original evaluation outputs were changed. No files
were staged. The staged manifest remains unchanged, and the staged diff
SHA-256 remains:

`d07f1e23abccd197402780542e0081025d12d35427ed9b418cf1291a97c8d980`

# XLabs AI Guide Capstone Rubric Audit

**Audit snapshot:** 2026-11-07
**Branch:** `feat/synthetic-evaluation`
**Rubric reference:** [Buildcamp Capstone Rubric](./BUILDCAMP_CAPSTONE_RUBRIC.md)

This is an evidence audit, not an official grade. The rubric source provides
criterion names and maximum points, but no scoring-level descriptors.
Accordingly, point estimates are **Not Verified**; presence of an implementation
does not establish a particular award.

## Repository and submission boundary

At the start of final curation, the staged index contained these eight paths:

- **Staged modifications:** `.gitignore`, `README.md`, `agent.py`.
- **Staged additions:** `evals/retrieval/EVALUATION_REPORT.md`,
  `evals/retrieval/data/queries.json`, `evals/retrieval/run.py`,
  `evals/synthetic/data/generated_cases.json`, and
  `tests/test_agent_instructions.py`.

The final curated manifest retains those eight paths, includes the updated
README content, and adds this audit and the rubric reference.

The current application and manual-evaluation implementation and evidence
remain tracked at `HEAD` and are not removed from Git. Relevant unchanged
tracked paths include `app.py`, `tools.py`, `data/`, `tests/test_tools.py`,
`evals/manual/`, `.python-version`, `pyproject.toml`, `uv.lock`,
`.env.example`, and the assessment screenshot.

The following are **untracked** and are not part of the staged submission:

- `evals/synthetic/EVALUATION_REPORT.md`,
  `evals/synthetic/generate.py`, `evals/synthetic/run.py`, and saved synthetic
  outputs other than `generated_cases.json`.
- `evals/manual/data/judge_evaluated_v2.csv` and
  `evals/manual/data/results_smoke_5.json`.
- `experiments/` and its saved results.
- Experimental tests under `tests/` for structured output, PydanticAI,
  structured capture, and synthetic evaluation.

These artifacts are preserved in the worktree. Their existence does not make
them part of the staged submission; do not stage them incidentally.

## Evidence notes

### Application, tools, and Agent mode

- `app.py` presents Service Connectivity, Pod Troubleshooting, and DNS
  Resolution scenarios, accepts a learner response, calls `agent()` and
  displays its text response and tool-call history. It calls the default mode
  without enabling Structured Output.
- `tools.py` implements three distinct tools:
  - `search_docs` searches the local Minsearch index and returns up to five
    results with document IDs, titles, symptoms, and source URLs.
  - `read_doc` returns the full local documentation record for a document ID.
  - `get_scenario` returns a saved scenario by ID.
- The current staged `agent.py` retains the text-output path and its
  instruction improvements. Structured Output is an opt-in experimental path
  (`structured_output=False` by default), is not called by `app.py`, and is
  not described as production app behavior in `README.md`.
- The tracked knowledge base contains three Kubernetes troubleshooting
  documents and three saved scenarios. Existence and code establish the local
  implementation; they do not establish completeness or broad retrieval
  quality.

### Tests, dependencies, and reproducibility

- `tests/test_tools.py` is tracked and exercises local saved-scenario
  retrieval.
- `tests/test_agent_instructions.py` is staged and uses a fake Responses
  client. Its input fixture,
  `evals/synthetic/data/generated_cases.json`, is also staged; the test and
  required fixture are both present in the submission index.
- During Step 4B, the two offline tests passed in the existing environment
  (`2 passed in 3.25s`); this is historical evidence.
- `pyproject.toml`, `uv.lock`, and `.python-version` are tracked. The README
  documents Python 3.13+, `uv sync`, and offline/API-backed test distinctions.
  No missing dependency or fixture for the two staged offline tests was
  identified.
- In Step 7, the complete Git index was exported with
  `git checkout-index --all` to a fresh directory outside the repository.
  `uv sync --frozen` succeeded there, installing 187 packages, and the two
  offline tests passed (`2 passed in 4.33s`). The snapshot had no `.env`;
  OpenAI- and Logfire-named environment variables were removed from the test
  process. uv warned that hardlinking was unavailable and fell back to copying.
- Step 7 verified locked installation and the offline tests from the exact
  staged snapshot, but did not use a clean Git clone, launch Streamlit, or
  verify live OpenAI API operation. The app and API-backed tests require a
  user-provided `OPENAI_API_KEY`; `.env.example` contains a placeholder, not a
  credential.
- Before/after checks confirmed the original Git status, staged manifest,
  staged diff fingerprint, and tracked worktree diff fingerprint were
  unchanged by Step 7.
- The README now records the Step 4B combined result for
  `tests/test_tools.py` and `tests/test_agent_instructions.py`: **2 passed in
  3.25s**, explicitly as historical evidence, and separately records the
  Step 7 result.

### Manual evaluation evidence

The tracked manual evaluation set has 51 scenario rows. `results.json` contains
51 Agent responses with no recorded execution errors. `results_labeled.json`
contains 51 records, of which 25 have labels: 24 `good` and 1 `bad`.
`judge_evaluated.csv` contains those 25 reviewed cases; its saved labels agree
on 24/25 cases (96%) with one disagreement.

The manual labeling UI supports labels, failure categories, and evidence
comments. The repository does not establish reviewer identity, an independent
review process, or inter-rater agreement. These are human-reviewed labels, not
demonstrated independently validated ground truth. The sample is small and
imbalanced, and the 96% figure is descriptive.

The README attributes the earlier 22/25 comparison to the project owner's
execution record; the initial V1 result and original prompt diff are not
independently preserved. The alternate `judge_evaluated_v2.csv` is untracked
and is not necessary to the tracked README claim.

Manual evaluation of Agent responses is not end-user feedback collection. No
product feedback channel or user feedback dataset is evidenced.

### Retrieval and synthetic evidence

The staged retrieval report, runner, and query dataset document a direct,
offline `search_docs()` evaluation, separate from Agent response evaluation.
The report records **2/3 Top-1** across three queries and explicitly reports
the Service-routing miss: `debug-services` ranked third. It also separates two
exploratory Service-query reformulations from the baseline metric and
acknowledges the small corpus/query-set limitation. The baseline was not rerun
for this audit.

`generated_cases.json` is staged and contains six synthetic cases and
reference assessments. The untracked `evals/synthetic/generate.py` shows that
the references were generated through an LLM call and labels generated
references provisional until manual review. The staged data alone does not
prove hand-crafted provenance or independent validation. The synthetic
evaluation report, runner, and saved results remain untracked and are not
included in the staged submission.

### Monitoring and infrastructure

`agent.py` configures Logfire, instruments OpenAI, and records assessment and
tool-call spans. The README documents a dashboard observation from October 26,
2026 (42 LLM calls, 2.735 seconds average duration, 40.04K input tokens, and
4,919 output tokens). These are historical figures, not a live check or proof
that a deployment or current trace collection is running.

No CI/CD workflow, Dockerfile, Docker Compose file, Makefile, or cloud
deployment manifest was found. The screenshot documents the Streamlit
interface at a point in time; it does not demonstrate cloud deployment or
current availability.

## Criterion-by-criterion audit

For all criteria, point estimates are **Not Verified** because the supplied
rubric reference has no grading-level descriptors. Status describes evidence
coverage, not a score.

### Core criteria

| ID / maximum | Status | Implementation evidence and repository paths (Git state) | Confirmed missing conditions / smallest useful action | Estimated points |
|---|---|---|---|---|
| **C1 Problem Description — 2** | Partial | Problem, learner value, and intended use are described in `README.md` (staged); three app scenarios are in `app.py` (tracked, unchanged). | No outcome study or user validation is documented. If available, add concise evidence from actual intended users without overstating results. | Not Verified |
| **C2 Knowledge Base & Retrieval — 2** | Partial | Three local documents in `data/kubernetes_troubleshooting_docs.json` and Minsearch tools in `tools.py` (both tracked, unchanged); three scenarios in `data/kubernetes_scenarios.json` (tracked, unchanged); retrieval runner/query/report staged under `evals/retrieval/`. | Baseline is only three queries and misses the Service-routing query (rank 3); corpus is only three documents. Expand a reviewed fixed query set before making broader quality claims. | Not Verified |
| **C3 Agents & LLM — 3** | Evidenced | OpenAI Responses API loop, tool use, and default text behavior in `agent.py` (staged); app call in `app.py` (tracked, unchanged); saved manual Agent outputs in `evals/manual/data/results.json` (tracked, unchanged). | Current live API operation is not verified by this audit. Preserve the text default; keep Structured Output labeled experimental and opt-in. | Not Verified |
| **C4 Code Organization — 2** | Partial | App, tools, Agent, manual evaluation code, and tests are separated into `app.py`, `tools.py`, `agent.py`, `evals/manual/`, and `tests/` (tracked or staged). | Structured Output experiment remains in `agent.py`; synthetic and PydanticAI source/results are untracked. Keep the existing boundary documented and make any later isolation narrowly scoped. | Not Verified |
| **C5 Testing — 2** | Partial | `tests/test_tools.py` (tracked, unchanged); `tests/test_agent_instructions.py` and its required generated-case fixture (both staged). Step 4B historical result: 2 passed in 3.25s. Step 7 exact staged-index snapshot result: 2 passed in 4.33s after `uv sync --frozen` installed 187 packages. | API-backed tests require credentials and were not part of the offline verification. Streamlit and live API operation were not tested. | Not Verified |
| **C6 Evaluation — 3** | Partial | Manual scenarios, Agent results, labels, and judge comparison in `evals/manual/data/` (tracked, unchanged); retrieval report/query/runner staged under `evals/retrieval/`; synthetic cases staged. | Manual sample has 25 labels, 24 good/1 bad, undocumented reviewer independence, and one disagreement. Retrieval sample is 2/3 on three queries. Synthetic references are model-generated/provisional per untracked generator; synthetic report/results are untracked. Document provenance and limitations; do not call labels independently validated ground truth. | Not Verified |
| **C7 Monitoring — 2** | Partial | Logfire configuration, OpenAI instrumentation, and session/tool spans in `agent.py` (staged); dated historical figures in `README.md` (staged). | No current monitoring check or current trace-collection evidence is available. Keep the historical qualifier; if current operation matters, record a dated, access-appropriate verification. | Not Verified |
| **C8 Reproducibility — 2** | Partial | `.python-version`, `pyproject.toml`, `uv.lock`, `.env.example` (tracked, unchanged); setup and test instructions in `README.md` (staged); offline test and fixture staged. In Step 7, `git checkout-index --all` exported the complete index to a fresh external directory; `uv sync --frozen` installed 187 packages and the two offline tests passed in 4.33s. The snapshot contained no `.env`, and repository state fingerprints remained unchanged. | Exact staged-snapshot installation and offline tests are verified. A clean Git clone, live Streamlit launch, and live OpenAI API operation were not verified. | Not Verified |

### Bonus criteria

| ID / maximum | Status | Implementation evidence and repository paths (Git state) | Confirmed missing conditions / smallest useful action | Estimated points |
|---|---|---|---|---|
| **B1 Hand-crafted Ground Truth Evaluation Dataset — +2** | Partial | 51 manual evaluation questions in `evals/manual/data/scenarios.csv` and human labels/comments in `results_labeled.json` (tracked, unchanged); six synthetic reference cases in `evals/synthetic/data/generated_cases.json` (staged). | Synthetic references were LLM-generated, not established as hand-crafted or independently reviewed; manual labels' provenance/independence is undocumented. Record review provenance and validate the intended reference set before claiming ground truth. | Not Verified |
| **B2 Manual Evaluation Against Ground Truth — +2** | Partial | Manual labeling UI in `evals/manual/app.py`; 25 labeled cases in `results_labeled.json`; saved comparison in `judge_evaluated.csv` (all tracked, unchanged). README documents 24/25 agreement. | This is documented human review, but no independent ground-truth or reviewer process is evidenced; sample is imbalanced. Clarify who reviewed and what reference standard was applied, if known. | Not Verified |
| **B3 User Feedback Collection — +1** | Missing | No end-user feedback feature or feedback dataset found. The manual labeler in `evals/manual/app.py` is an evaluation tool, not evidence of product-user feedback. | No in-product or other user feedback collection is evidenced. Do not equate evaluator labels with learner feedback. | Not Verified |
| **B4 Monitoring Logs Converted to Evaluation Data — +2** | Missing | Logfire spans and historical dashboard figures are documented in `agent.py` and `README.md`. | No pipeline or saved evaluation dataset derived from monitoring logs was found. This would require a separately defined, privacy-conscious conversion workflow. | Not Verified |
| **B5 Docker Containerization — +1** | Missing | No Dockerfile found. | No container build or run configuration. Only add if rubric value justifies dependency/configuration work and the image can be verified. | Not Verified |
| **B6 Docker Compose Workflow — +2** | Missing | No Compose file found. | No multi-service Compose workflow. There is no evidenced multi-container deployment to orchestrate. | Not Verified |
| **B7 Makefile — +1** | Missing | No Makefile found. | No task aliases exist. A small Makefile could standardize setup/offline-test commands, but it should not duplicate existing instructions without a clear benefit. | Not Verified |
| **B8 uv Dependency Management — +1** | Evidenced | `pyproject.toml`, `uv.lock`, `.python-version`, and `uv` setup commands in `README.md` (tracked or staged). Step 7 verified `uv sync --frozen` from the exact staged-index snapshot; 187 packages installed. | A clean Git clone was not used, but the staged snapshot's locked dependency installation succeeded. Live app operation was not part of this verification. | Not Verified |
| **B9 CI/CD — +2** | Missing | No `.github/workflows/` files or other CI workflow configuration found. | No automated pipeline is present. A minimal CI workflow for offline tests is the smallest low-behavior-risk improvement if time permits. | Not Verified |
| **B10 Working Agent UI — +1** | Partial | Streamlit UI implementation in `app.py` and screenshot `xlabs-ai-guide-streamlit-assessment.png` (tracked, unchanged); README describes its local behavior (staged). | Screenshot is historical evidence, not proof of current operation or cloud deployment. A local launch/smoke check can verify current UI without implying deployment. | Not Verified |
| **B11 Cloud Deployment — +2** | Missing | README explicitly says no cloud deployment is claimed; no deployment manifests/configuration found. | No cloud service, URL, or deployment evidence. Do not infer deployment from the screenshot. | Not Verified |

## Scorecards and total

### Core scorecard

| Criterion | Status | Estimated points |
|---|---|---|
| C1 Problem Description (2) | Partial | Not Verified |
| C2 Knowledge Base & Retrieval (2) | Partial | Not Verified |
| C3 Agents & LLM (3) | Evidenced | Not Verified |
| C4 Code Organization (2) | Partial | Not Verified |
| C5 Testing (2) | Partial | Not Verified |
| C6 Evaluation (3) | Partial | Not Verified |
| C7 Monitoring (2) | Partial | Not Verified |
| C8 Reproducibility (2) | Partial | Not Verified |
| **Core total (maximum 18)** |  | **Not Verified** |

### Bonus scorecard

| Criterion | Status | Estimated points |
|---|---|---|
| B1 Hand-crafted Ground Truth Evaluation Dataset (+2) | Partial | Not Verified |
| B2 Manual Evaluation Against Ground Truth (+2) | Partial | Not Verified |
| B3 User Feedback Collection (+1) | Missing | Not Verified |
| B4 Monitoring Logs Converted to Evaluation Data (+2) | Missing | Not Verified |
| B5 Docker Containerization (+1) | Missing | Not Verified |
| B6 Docker Compose Workflow (+2) | Missing | Not Verified |
| B7 Makefile (+1) | Missing | Not Verified |
| B8 uv Dependency Management (+1) | Evidenced | Not Verified |
| B9 CI/CD (+2) | Missing | Not Verified |
| B10 Working Agent UI (+1) | Partial | Not Verified |
| B11 Cloud Deployment (+2) | Missing | Not Verified |
| **Bonus total (itemized maximum 17)** |  | **Not Verified** |

**Total supported estimate: Not Verified.** The user-provided summary states a
course-stated maximum of 33 points and an itemized maximum of 35 points (18
Core + 17 Bonus), with a reported threshold of 12. The supplied itemized
maxima add to 35. The separately reported 33-point course maximum remains
unresolved; this audit does not invent an explanation or reconciliation.
Individual point awards also remain unverified because scoring-level
descriptors were not provided.

## Confirmed blockers and opportunities

### Submission and reproducibility blockers

- No missing dependency or fixture for the two staged offline tests was
  identified: `pyproject.toml` and `uv.lock` are tracked, and
  `tests/test_agent_instructions.py` plus
  `evals/synthetic/data/generated_cases.json` are staged together.
- The two offline tests passed in Step 4B (2 passed in 3.25s) and again from
  the exact staged-index snapshot in Step 7 (2 passed in 4.33s after
  `uv sync --frozen` installed 187 packages). A clean Git clone was not used;
  live Streamlit and OpenAI API operation remain unverified. This is not a
  confirmed missing-file or dependency blocker for the staged offline scope.
- Current user-facing Agent behavior is text-based by default. Structured
  Output remains experimental in the staged `agent.py`; it is not activated by
  the app.
- Untracked synthetic reports/results and experiments are not part of the
  staged submission. Preserve them and avoid broad staging.
- API-backed app operation and tests require a user-supplied key and were not
  verified here. Historical Logfire figures do not prove current operation.

### Bonus opportunities ranked

| Priority | Opportunity | Potential maximum | Effort / regression risk | Rationale |
|---:|---|---:|---|---|
| 1 | Minimal CI for offline tests (B9) | +2 | Low-to-moderate effort; low Agent behavior risk | Adds repeatable automated verification without changing the app or calling paid APIs. Verify the workflow itself before claiming CI evidence. |
| 2 | Record and validate evaluation provenance (B1/B2, supports C6) | Up to +4 itemized | Moderate review effort; no runtime risk | Highest evidence value: distinguish generated references, manual reviewer labels, and independently reviewed ground truth. Do not relabel existing data without evidence. |
| 3 | Optional clean-clone and local UI smoke verification (C5/C8/B10) | Supports Core evidence and B10 | Low-to-moderate effort; no Agent behavior change, but UI/API smoke needs credentials | Stronger evidence beyond the verified staged-index install and offline tests; not required to claim that the staged snapshot reproduces those checks. |
| 4 | Makefile with a few documented commands (B7) | +1 | Low effort and low risk | Convenient but small value; avoid redundant wrappers unless they simplify actual use. |
| 5 | Docker and Compose (B5/B6) | +3 | Moderate-to-high effort; configuration and secret-handling risk | Consider only if rubric priorities warrant container work; local single-app use does not yet evidence a Compose need. |
| 6 | Monitoring-log evaluation pipeline (B4) | +2 | High effort and data/privacy risk | Requires a careful definition of log selection, sanitization, labels, and evaluation methodology. |
| 7 | End-user feedback collection (B3) | +1 | Product-scope and privacy risk | Not equivalent to evaluator labeling; defer unless genuine learner feedback is part of the intended product. |
| 8 | Cloud deployment (B11) | +2 | Highest operational and credential risk | No deployment is claimed or configured. Defer absent a clear rubric-driven requirement and time for operational verification. |

The local Agent UI (B10) and `uv` setup (B8) already have implementation
evidence. Improve only the current-operation/reproducibility evidence rather
than adding Agent features.

## Minimal implementation sequence

1. Keep the existing staged application, manual evidence, and text Agent
   instructions intact. Continue to exclude secrets, downloaded course code,
   generated smoke outputs, and experiments from staging.
2. Record the distinct Step 4B historical result (2 passed in 3.25s) and Step 7
   staged-index snapshot result (2 passed in 4.33s; 187 packages installed)
   without conflating them. Step 7 verifies offline setup and tests, not a
   clean Git clone, Streamlit launch, or live API operation.
3. No further installation or offline test run is needed to verify the exact
   staged snapshot. If stronger evidence is desired, perform a separate clean
   clone or local UI smoke check later, with API use and credentials handled
   explicitly; preserve the existing datasets.
4. Clarify evaluation provenance and limitations from documented facts only:
   manual labels are not independently validated ground truth, synthetic
   references were generated and are provisional absent review evidence, and
   retrieval results cover only three queries.
5. If time and rubric value allow, add a minimal CI workflow that runs only
   offline tests. Defer Docker, Compose, feedback collection, log conversion,
   and cloud deployment unless the official rubric descriptors or project
   requirements justify their additional scope.

## Recommended next implementation action

The exact staged-index snapshot has now passed `uv sync --frozen` and the two
offline tests (**2 passed in 4.33s**, 187 packages installed). Step 4B's
earlier **2 passed in 3.25s** remains historical evidence. A clean Git clone,
live Streamlit launch, and live OpenAI API operation remain unverified.

## Historical status clarification

The findings above that Docker, Docker Compose, a Makefile, and CI configuration
were missing describe repository evidence available at the time of this audit;
they are preserved as historical findings. Later implementation and runtime
verification are recorded in
[`BONUS_RUNTIME_VERIFICATION.md`](./BONUS_RUNTIME_VERIFICATION.md): B5 Docker,
B6 Docker Compose, and B7 Makefile are **PASS**; B10 Working Agent UI is
**PASS / Supported provisionally**. B9 CI/CD configuration now exists, but
successful GitHub Actions execution remains unverified. These later results do
not revise the historical findings or scores above.

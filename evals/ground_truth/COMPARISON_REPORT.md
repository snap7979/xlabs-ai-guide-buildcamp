# Ground Truth Review and Agent Comparison

## Status and provenance

This report compares saved Agent responses with the ten assessment criteria
the user states were reviewed and approved in ChatGPT on 2026-11-08. The
approval provenance is user-reported; no reviewer name is recorded. Findings
below are **PROVISIONAL — AWAITING USER REVIEW**. They are comparisons, not
final Good/Bad labels or official rubric scores.

The original synthetic scenarios, learner answers, and generated references
remain LLM-generated material, not independently human-authored ground truth.
The four manual prompts are existing records from `evals/manual/data/scenarios.csv`;
repository evidence does not establish their author. The approved expected
criteria are recorded separately from all original inputs and references in
[`data/reviewed_cases.json`](./data/reviewed_cases.json).

## Verification method

- Verified all six synthetic IDs and their original scenario/answer against
  `evals/synthetic/data/generated_cases.json`, the corresponding source IDs
  against `data/kubernetes_troubleshooting_docs.json`, and matching
  `case_id` inputs and error-free saved outputs in
  `evals/synthetic/data/agent_results_current_baseline.json`.
- Verified the four manual prompt strings against rows 30, 31, 33, and 36 of
  `evals/manual/data/scenarios.csv`. Their `input.question` fields match
  exactly in records with the same 1-based positions in both
  `evals/manual/data/results.json` and `results_labeled.json`; saved response
  texts also match between those two files.
- The synthetic `agent_results.json` contains the same six case IDs but
  different response texts from `agent_results_current_baseline.json`.
  This report consistently compares the timestamped current-baseline
  snapshot; it does not merge or treat the two runs as one.
- Source support below refers to the compact documentation records in
  `data/kubernetes_troubleshooting_docs.json`. No source records were changed.

## Per-case comparison

| Case | Saved Agent response vs approved criteria — **PROVISIONAL — AWAITING USER REVIEW** |
|---|---|
| `debug-running-pods-2` | **Aligned:** credits the log check, identifies the unsupported healthy-Pod conclusion, and recommends checking Pod status/events (`describe`) and previous logs. The response does not assert a specific root cause. |
| `debug-services-2` | **Aligned:** treats incorrect ports as a reasonable hypothesis and recommends selector/label, endpoint, and port checks without claiming a confirmed cause. **Discrepancy:** calls no misconception demonstrated despite the learner explicitly dismissing label/selector checks. It does not compare the Service path with direct Pod connectivity. |
| `dns-services-pods-2` | **Aligned:** flags the “namespace should not be specified” statement and recommends lookup and Pod DNS configuration checks. **Discrepancy:** credits a DNS-root-cause inference from the IP/name contrast and treats it as demonstrated understanding; the approved criterion says not to credit unverified root-cause certainty. It recommends a qualified name but does not explain same-namespace versus cross-namespace behavior. It does not claim DNS failure is confirmed. |
| `debug-running-pods-1` | **Aligned:** credits status/events and recommends previous logs; it does not invent a restart cause. **Discrepancy:** says logs were not discussed, although the learner mentions logs conditionally (“If the logs don't provide enough information”); the response does not distinguish mentioning a possible check from having executed it. It repeats `exec` as a next step but omits the approved crash-loop limitation. |
| `manual-scenarios-row-33` | **Aligned:** flags the “Running means healthy” claim and recommends events/logs; it does not credit any diagnostic step from the learner. **Partial:** discusses Pod status versus application health, but does not explicitly explain Running versus Ready or give a readiness check. The repository's compact Pod documentation record does not contain that Running/Ready distinction, so this part of the approved criterion is not supported by the stored summary. |
| `debug-services-1` | **Aligned:** credits selector/label and endpoint checks. **Discrepancy:** does not credit the learner's port comparison or direct Pod-IP test, and instead raises DNS as an omitted check and recommends DNS investigation. This introduces an unsubstantiated alternative direction rather than focusing further on the Service traffic path; no confirmed DNS cause is asserted. |
| `manual-scenarios-row-30` | **Aligned:** marks the immediate node restart as unjustified and recommends selector and endpoint checks; it does not say restarting nodes would fix the issue. **Discrepancy:** credits the learner with identifying “a critical issue” (the absence of endpoints), a fact in the scenario and not in the learner's answer. It recommends direct Pod-IP testing but does not clearly call for inspection of the selected target Pods. |
| `manual-scenarios-row-31` | **Partial:** credits selector inspection, flags “targetPort never matters,” and recommends checking endpoints and comparing the Service `port` and `targetPort` with the application port. It does not explicitly explain the distinction between Service `port` and `targetPort`, so that criterion is not fully satisfied. It does not claim the port caused the observed failure. |
| `manual-scenarios-row-36` | **Partial:** recommends Pod-level name lookup and `resolv.conf` inspection, plus selector/endpoint checks. **Discrepancy:** calls focusing only on port a misconception, whereas the approved criterion treats it as an omission unless the learner asserts a false technical belief. It does not explain why IP success/name failure specifically warrants DNS investigation or address namespace inspection. It does not assert a confirmed cause. |
| `dns-services-pods-1` | **Aligned:** credits Pod-level DNS lookup, `resolv.conf`, DNS Pods, and DNS logs; identifies Service endpoints as an omitted useful check and recommends checking them. It does not claim DNS is definitively the root cause. |

## Evidence gaps and record notes

- The stored DNS documentation record mentions qualified Service DNS names,
  lookup tests, and `resolv.conf`, but does not explicitly explain unqualified
  same-namespace lookup versus cross-namespace lookup. The approved nuance for
  `dns-services-pods-2` should be checked against a fuller source before
  treating that explanation as source-grounded.
- The stored Pod documentation summary recommends Pod status/events and logs,
  but does not explicitly contrast Running with Ready or prescribe readiness
  checks. The matching manual case response exists, but the approved
  Running/Ready criterion exceeds the detail in the stored summary.
- For `debug-running-pods-1`, the stored record says `exec` is for inspecting
  a running container when image and permissions allow it. It does not name
  CrashLoopBackOff; the approved statement that a crash loop can prevent
  `exec` is consistent with that limitation but is not stated verbatim in the
  summary.
- The manual records at rows 31 and 33 already have `good` labels in
  `results_labeled.json`. Those labels are unchanged and are not treated as
  gold-standard assessments. Rows 30 and 36 have no saved label.
- No matching response was missing, and all selected saved responses had no
  recorded execution error. Synthetic response mapping is unambiguous by
  `case_id`; manual mapping was verified by exact prompt match at the recorded
  row index.
- The alternate synthetic `agent_results.json` responses differ from the
  current-baseline responses. The SHA-256 references in the structured
  dataset identify the version actually compared.

No final labels or scores are assigned. User review is still needed for the
provisional per-case comparisons and the noted source-detail gaps.

## Subsequent human review record

The provisional findings and recommendations above are preserved as the
historical Copilot comparison. Final human-approved labels are recorded
separately in [`HUMAN_REVIEW_REPORT.md`](./HUMAN_REVIEW_REPORT.md) and
[`data/human_review_labels.json`](./data/human_review_labels.json); they do
not replace or silently revise the provisional analysis above.

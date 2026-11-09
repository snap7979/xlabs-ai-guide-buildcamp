# Ground Truth Human Review

## Purpose and methodology

This report records the human project owner's final labels for the ten reviewed
Ground Truth cases after review of the saved Agent responses with AI-assisted
discussion. The decisions are human-approved; the discussion and comparison
notes were AI-assisted. This is a documentation record, not a new Agent or
Judge evaluation.

The original approved assessment criteria and response references remain in
[`data/reviewed_cases.json`](./data/reviewed_cases.json). The labels, explicit
owner rationales where provided, separately attributed AI-assisted notes, and
response hashes are stored in
[`data/human_review_labels.json`](./data/human_review_labels.json). Human
rationales are included only for cases 2, 3, 6, and 7, for which the project
owner supplied explicit reasons. For other cases, no separate owner rationale
is inferred from the AI-assisted discussion.

## Final decisions

| # | Case ID | Human-approved label | Prior Copilot provisional recommendation |
|---|---|---|---|
| 1 | `debug-running-pods-2` | Good | Good |
| 2 | `debug-services-2` | Bad | Bad |
| 3 | `dns-services-pods-2` | Bad | Bad |
| 4 | `debug-running-pods-1` | Good | Bad — disagreement |
| 5 | `manual-scenarios-row-33` | Good | Bad — disagreement |
| 6 | `debug-services-1` | Bad | Bad |
| 7 | `manual-scenarios-row-30` | Bad | Bad |
| 8 | `manual-scenarios-row-31` | Good | Good |
| 9 | `manual-scenarios-row-36` | Good | Bad — disagreement |
| 10 | `dns-services-pods-1` | Good | Good |

**Totals:** 10 reviewed cases; 6 Good; 4 Bad.

The labels assess the Agent's assessment against the approved criteria, not
whether the learner's original answer was correct.

## Explicit human rationales

The following are the project owner's explicit reasons, recorded separately
from AI-assisted assessment notes:

- **Case 2 — `debug-services-2` (Bad):** Agent failed to identify the learner's
  explicit misconception about ignoring Service selectors and labels.
- **Case 3 — `dns-services-pods-2` (Bad):** Agent over-credited an unverified
  DNS diagnosis and did not explain the scope of Kubernetes Service-name
  resolution.
- **Case 6 — `debug-services-1` (Bad):** Agent failed to credit the learner's
  port comparison and direct Pod-IP test, and redirected troubleshooting
  toward DNS without sufficient evidence.
- **Case 7 — `manual-scenarios-row-30` (Bad):** Agent credited the learner with
  identifying missing endpoints, although that information appeared only in
  the scenario.

No separate detailed owner rationale was supplied for the other six labels.
In particular, Cases 4 and 5 were approved Good despite the initial provisional
Bad recommendations. Case 9 was approved Good despite the initial provisional
Bad recommendation; the project owner supplied no separate detailed reason
for that disagreement. No explanation for these disagreements is inferred
here.

## AI-assisted analysis notes

These are notes from the prior provisional comparison, not direct quotations
or rationales attributed to the project owner:

1. **`debug-running-pods-2` — prior Good:** The comparison found that the
   response credits log checking, rejects the unsupported healthy-Pod
   inference, recommends status/events and previous logs, and states no
   specific cause.
2. **`debug-services-2` — prior Bad:** The response treats ports as a
   hypothesis and recommends selector/label, endpoint, and port checks, but
   misses the learner's explicit dismissal of selector checks and omits the
   Service-versus-direct-Pod connectivity comparison.
3. **`dns-services-pods-2` — prior Bad:** The response flags the namespace
   claim and recommends DNS checks, but over-credits the unverified DNS
   diagnosis and does not explain same-namespace versus cross-namespace
   resolution.
4. **`debug-running-pods-1` — prior Bad:** The response credits status/events
   and recommends previous logs, but says logs were not discussed despite the
   learner's conditional mention and does not qualify `exec` for a restart
   loop.
5. **`manual-scenarios-row-33` — prior Bad:** The response flags the
   Running-means-healthy claim and recommends events/logs, but does not explain
   Running versus Ready or recommend readiness checks.
6. **`debug-services-1` — prior Bad:** The response credits selector and
   endpoint checks but misses the learner's port comparison and direct Pod-IP
   test, then raises DNS without sufficient support.
7. **`manual-scenarios-row-30` — prior Bad:** The response rejects restarting
   all nodes and recommends selector/endpoint checks, but credits the learner
   with a scenario fact and does not clearly call for target-Pod inspection.
8. **`manual-scenarios-row-31` — prior Good:** The response credits selector
   inspection, flags the `targetPort` misconception, and recommends port
   checks, but does not explicitly explain Service `port` versus `targetPort`.
9. **`manual-scenarios-row-36` — prior Bad:** The response recommends DNS
   lookup and configuration checks but calls the port-only focus a
   misconception rather than an omission and does not explain why the symptom
   warrants DNS checks.
10. **`dns-services-pods-1` — prior Good:** The response credits Pod-level
    DNS lookup, `resolv.conf`, DNS Pods, and DNS logs, and recommends checking
    Service endpoints without claiming a definitive DNS cause.

The historical provisional classifications are preserved for comparison;
they have not been silently replaced. The three differences between the prior
recommendations and human-approved labels are cases 4, 5, and 9.

## Source provenance

Six cases use synthetic-source material from
`evals/synthetic/data/generated_cases.json`; the corresponding saved Agent
responses are explicitly pinned by case ID to
`evals/synthetic/data/agent_results_current_baseline.json`. This synthetic
case and reference material is identified in the repository as LLM-generated
and is not independently human-authored ground truth.

Four cases correspond to existing manual evaluation prompts at rows 30, 31,
33, and 36 of `evals/manual/data/scenarios.csv`; saved Agent responses are
mapped to the matching records in `evals/manual/data/results.json`. The saved
files do not establish that the manual prompts were independently
human-authored. No authorship is inferred for any original scenario or
learner input.

Response text SHA-256 values and exact source locators are recorded per case
in the label dataset. Existing labels in `results_labeled.json` are not
changed or treated as Ground Truth labels by this review.

## Known limitations and scope

- The stored Kubernetes documentation summary does not explicitly explain
  same-namespace versus cross-namespace Service-name resolution, which limits
  source support for DNS namespace criteria in cases 3 and 9.
- The stored Pod documentation summary does not explicitly contrast Running
  with Ready or prescribe readiness checks, which limits source support for
  case 5.
- The compact Pod summary describes `exec` for a running container subject to
  image and permission constraints, but does not name CrashLoopBackOff.
- These ten cases are a reviewed comparison set, not a representative sample
  or measure of overall Agent accuracy. No overall accuracy claim is made.
- This review does not establish B1 (a hand-crafted Ground Truth dataset):
  synthetic references are LLM-generated and manual-prompt authorship is not
  established. It also does not establish B2 (an independent ground-truth or
  reviewer process). Both remain **Not Verified**; this report awards no
  official Buildcamp Bonus points.
- No official Buildcamp Bonus points are awarded or implied.

## Offline verification

Run the standard-library-only verifier from the repository root:

```sh
python evals/ground_truth/verify_human_review.py
```

The script checks case identity/order and labels, response mappings and
hashes, input provenance, explicit-rationale attribution, and fixed SHA-256
fingerprints for the original source/result datasets and existing labels.

## Subsequent evidence clarification

The earlier B1/B2 **Not Verified** wording reflects the evidence assessment at
that time. B1 is now **provisionally supported** by ten human-approved Ground
Truth assessment criteria. Scenario inputs have mixed provenance: six
synthetic-source cases and four cases sourced from earlier manual evaluation
records. Human approval does not establish that every scenario or learner
answer was originally written by a human. Whether this qualifies as
“hand-crafted” remains unresolved because detailed official grading
descriptors have not been verified. B2 is supported by ten human-approved
evaluations against the Ground Truth criteria. The final decisions remain six
Good and four Bad; the review was AI-assisted, with final labels approved by
the project owner. No official Buildcamp Bonus points have been awarded.

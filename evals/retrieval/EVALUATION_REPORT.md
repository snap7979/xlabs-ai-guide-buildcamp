# Offline Retrieval Evaluation

## Purpose and architecture

This evaluation checks whether XLabs AI Guide's existing `search_docs()` ranks
the expected local Kubernetes troubleshooting note first for a small set of
direct queries. It is separate from Agent response evaluation.

The runner reads the labeled query records in `data/queries.json` and calls
`search_docs()` directly from `tools.py`. That function searches the locally
loaded JSON records with the existing `minsearch.Index`, fitted over title,
symptoms, guidance, commands, and source title as text fields, and document ID
and category as keyword fields. The runner records the ordered document IDs,
the expected document's rank, and Top-1 accuracy. It does not invoke the Agent,
read documents through `read_doc()`, or make OpenAI calls.

## Baseline results

The baseline contains three queries, one for each of the three source
documents:

| Query | Expected document ID | Observed rank |
|---|---|---:|
| "A Pod is unhealthy or its container keeps restarting." | `debug-running-pods` | 1 |
| "A Service cannot route traffic to its Pods." | `debug-services` | 3 |
| "A Service name fails to resolve even though access by IP works." | `dns-services-pods` | 1 |

**Baseline Top-1 Accuracy: 2/3 (66.7%).**

## Service-query diagnosis

Two additional offline searches were run specifically to investigate the
baseline Service miss. They are diagnostic observations, not part of the
baseline metric:

| Diagnostic query | Expected document ID | Observed rank |
|---|---|---:|
| "A Service cannot route traffic to its Pods." | `debug-services` | 3 |
| "Clients cannot reach an application through its Kubernetes Service address, but the Pod IP works." | `debug-services` | 1 |
| "A Kubernetes Service cannot forward requests to its application Pods." | `debug-services` | 3 |

These observations show sensitivity to query wording: the query mentioning
clients being unable to reach an application through its Service address ranks
`debug-services` first, while the two formulations about routing or forwarding
requests rank it third. This small set demonstrates variation, not a general
measure of robustness.

### Possible explanations (hypotheses)

- The successful wording overlaps with the `debug-services` symptom text,
  which says clients cannot reach the application through the Service address.
  Its reference to Pod IP also overlaps with that document's guidance to
  compare Service-path access with Pod IP access.
- The failing formulations use "route" or "forward requests," terms that do not
  appear in that document's symptom text. The competing DNS record mentions a
  Service name and access by IP, and the Pod record also contains Pod-related
  terms. Such overlap could contribute to their ranking.
- The index's tokenization or scoring may favor some terms or field matches
  over others.

These are hypotheses based on the visible query and indexed text. The
observations do not identify a proven cause: the current search code does not
expose per-document scores or explain the ranking.

## Limitations

- The corpus contains only three source documents.
- The baseline has only three labeled cases, one per document.
- The diagnosis adds only two additional Service-query formulations.
- The results are too small to establish broad relevance, paraphrase robustness,
  or generalization to other Kubernetes topics.
- The evaluation measures whether the expected document ranks first; it does
  not assess the usefulness or completeness of returned guidance.

## Follow-up recommendations

- Keep the current three baseline cases and their metric distinct from
  exploratory diagnostic queries.
- Expand the labeled query set with reviewed paraphrases for each document and
  representative ambiguous or near-miss queries.
- Track Top-1 accuracy and a ranked metric such as reciprocal rank, so
  expected documents returned below the first position are measured as well.
- When changing retrieval behavior, rerun the same fixed labeled set and
  compare results before and after; retain individual rankings for inspection.
- Keep the evaluation offline and focused on direct `search_docs()` results so
  retrieval quality remains distinguishable from Agent response quality.

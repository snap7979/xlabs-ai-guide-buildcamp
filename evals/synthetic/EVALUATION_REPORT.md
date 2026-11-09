# Synthetic Evaluation Report

## 1. Objective and methodology

This evaluation compares the XLabs AI Guide Agent's responses with reviewed
reference assessments for six synthetic Kubernetes troubleshooting cases. The
runner passes each case's scenario as context and its learner answer as the
answer to assess, without including the reference assessment in the Agent input.
It records each response and the Agent's tool-call history.

The review below is qualitative: it compares the saved Agent responses in
`data/agent_results.json` with the corresponding reviewed assessments in
`data/generated_cases.json`. It does not evaluate why a response took a
particular path.

## 2. Dataset

The dataset contains six cases, two for each of three local Kubernetes
documentation records:

- `debug-running-pods-1` and `debug-running-pods-2` — Debugging Running Pods
- `debug-services-1` and `debug-services-2` — Debugging Services
- `dns-services-pods-1` and `dns-services-pods-2` — DNS for Services and Pods

Each case includes a scenario, learner answer, reviewed reference assessment,
case ID, source document ID, and source URL.

## 3. Execution results

The saved results contain six Agent responses and six tool-call histories:
**6 successful runs, 0 execution failures**. Each record is keyed by its case
ID and includes the response and tool calls such as `search_docs` and
`read_doc`. The saved input to the Agent, defined in `run.py`, contains only
the scenario facts and learner answer; it does not include the reference
assessment.

Results are saved in `data/agent_results.json`. This report reviews the saved
run; it does not rerun the Agent.

## 4. Case-by-case comparison

### `debug-running-pods-1`

- **Reference:** Credits checking Pod status with `kubectl describe pod` and
  conditionally using `kubectl exec`; recommends checking logs and notes
  `exec` requires an accessible running container and suitable image and
  permissions.
- **Agent:** Credits `describe` and `exec`, but does not state the `exec`
  preconditions. It identifies logs as a check not discussed and recommends
  `kubectl logs pod-name`.
- **Comparison:** The Agent's log recommendation is consistent with the
  reference's next steps. The learner says, “If the logs don't provide enough
  information,” but does not explicitly state a `kubectl logs` command. The
  Agent's claim that logs were not mentioned is therefore somewhat imprecise:
  the topic is mentioned, but an explicit log check is not commanded.

### `debug-running-pods-2`

- **Reference:** Separately credits the learner for checking logs and flags
  the claim that no logs means the Pod is healthy as a misconception.
- **Agent:** Recognizes that the learner used `kubectl logs` and incorrectly
  inferred health from the empty output; it also identifies `describe` and
  previous logs as omitted checks.
- **Comparison:** The central distinction between the useful log check and
  the unsupported health conclusion is present in both. The Agent's
  demonstrated-understanding section combines the two points rather than
  clearly crediting the log check independently.

### `debug-services-1`

- **Reference:** Credits the selector, endpoints, port comparison, and Pod IP
  checks; recommends comparing connectivity through the Service from inside
  the cluster with access to a Pod IP.
- **Agent:** Credits the checks but shifts next steps toward DNS resolution
  and DNS Pod logs, and calls DNS a check not discussed.
- **Comparison:** That DNS shift is not the reference's prioritized follow-up.
  The local Service record points to comparing the Service path with Pod IP
  access. The saved tool history shows that the Agent retrieved the Service
  document and a DNS document; this alone does not establish that retrieval
  caused the response.

### `debug-services-2`

- **Reference:** Identifies the assumption that changing ports alone will
  resolve the issue as a misconception and lists the selector, endpoints, and
  Service-versus-Pod-IP comparison as checks not discussed.
- **Agent:** Identifies a misconception about redefining ports and recommends
  checking selectors, endpoints, and port mapping. It says the learner
  “acknowledge[s] that Pods are reachable directly,” which is stated in the
  scenario, not the learner answer; this may credit scenario context as
  demonstrated understanding.
- **Command check:** The requested malformed string
  `kubectl get endpointsSERVICE_NAME` is **not** in the saved response. The
  Agent instead wrote `kubectl get endpoints SERVICE_NAME`, with a space;
  that matches the command in the local Debugging Services record. Thus, the
  alleged malformed command is not confirmed by the saved files.

### `dns-services-pods-1`

- **Reference:** Credits DNS lookup, `/etc/resolv.conf`, DNS Pod availability,
  and the learner's stated DNS log check; recommends verifying Service
  endpoints.
- **Agent:** Credits the DNS lookup, resolver configuration, and DNS Pod
  availability, but does not explicitly credit the stated DNS log check. It
  recommends checking logs and Service endpoints.
- **Comparison and command check:** The Agent's endpoint command is
  `kubectl get endpoints SERVICE_NAME -n NAMESPACE`; the local DNS document's
  command field lists `kubectl get endpoints SERVICE_NAME` only. The added
  namespace argument means the command is not an exact match to that listed
  command. Since `agent.py` instructs the Agent to output only commands
  appearing exactly in a retrieved document's commands field, this is an
  observed deviation from that instruction. The recommendation to verify
  endpoints itself is supported by the local guidance. No conclusion is made
  here about retrieval causing the deviation.

### `dns-services-pods-2`

- **Reference:** Correctly states that a short Service name can resolve within
  the same namespace and that cross-namespace access needs an appropriately
  qualified name.
- **Agent:** Corrects the learner's claim that the namespace should never be
  specified, but says the full Service DNS name includes a namespace without
  clarifying that short names can work in the same namespace.
- **Comparison:** The Agent's explanation is incomplete relative to the
  reviewed reference. Its other recommendations include DNS lookup and
  Service selector/endpoints checks.

## 5. Confirmed observations

- **`debug-running-pods-1`:** The Agent omits the running/accessibility and
  image/permission preconditions for `kubectl exec`. The learner mentions
  logs conditionally but does not explicitly command a log check.
- **`debug-running-pods-2`:** The reference correctly distinguishes checking
  logs from the misconception that empty logs imply a healthy Pod. The Agent
  notices both but does not separate the demonstrated log check as clearly.
- **`debug-services-1`:** The Agent shifts toward DNS troubleshooting where
  the reference prioritizes comparing the Service path with Pod IP access.
- **`debug-services-2`:** The Agent may credit direct Pod reachability stated
  only in the scenario. The reported malformed
  `kubectl get endpointsSERVICE_NAME` command is not present; the saved
  response has the correctly spaced command
  `kubectl get endpoints SERVICE_NAME`.
- **`dns-services-pods-1`:** The Agent does not explicitly credit the
  learner's stated DNS log check. Its endpoint command
  `kubectl get endpoints SERVICE_NAME -n NAMESPACE` is not identical to the
  local command `kubectl get endpoints SERVICE_NAME`, despite the endpoint
  check being supported by the guidance.
- **`dns-services-pods-2`:** The Agent does not clarify that short Service
  names can resolve within the same namespace.

## 6. Reference assessment limitations and ambiguities

- In `debug-running-pods-1`, the learner mentions logs as a condition but does
  not explicitly state a log command. Whether this merits credit for a
  discussed check is ambiguous; the reference's next-step suggestion to check
  logs is reasonable. Likewise, the learner proposes `kubectl exec` but does
  not state its preconditions; the reference records those preconditions in
  the assessment, not in the learner's answer.
- In `debug-services-1`, the learner reports direct Pod IP connectivity but
  does not say they tested the Service from inside the cluster. The reference
  leaves that comparison as a next step, which distinguishes it from the
  completed checks.
- In `debug-services-2`, the Agent's direct-Pod-reachability credit is
  attributable to the scenario text, so it is an Agent evidence-attribution
  issue. The malformed endpoint command is not in the saved response and
  should not be treated as an Agent error in this run.
- In `dns-services-pods-1`, the reference credits reviewing DNS Pod logs,
  which the learner explicitly says they will do. The Agent recommends that
  same check but does not explicitly list it as demonstrated understanding.
  The Agent's endpoint recommendation is grounded as a diagnostic concept,
  while its exact command differs from the source command field; these are
  distinct observations.
- In `dns-services-pods-2`, the reference correctly captures the namespace
  nuance. The Agent's explanation is incomplete relative to that reference,
  rather than evidence that the reference itself is incorrect.

These are qualitative comparisons of the saved text. They do not determine
whether an observed response issue arose during retrieval, prompt
interpretation, or generation.

## 7. Follow-up items

### Retrieval Evaluation

- Evaluate whether the right local document is retrieved for each case and
  whether relevant command and guidance fields are available to the Agent.
- Measure retrieval relevance separately from response quality; the saved
  tool-call histories record document IDs but are not themselves a retrieval
  quality evaluation.

### Agent Improvements

- Preserve scenario facts as context and avoid presenting them as learner
  evidence.
- State `kubectl exec` preconditions when recommending or assessing it.
- Distinguish a learner's stated check from a misconception about what its
  result means.
- Keep recommendations focused on the applicable source guidance and use
  commands exactly as listed in retrieved documentation.
- Explain the same-namespace short-name behavior when assessing Service DNS
  namespace claims.

## 8. Limitations

This is a qualitative review of six synthetic cases and their saved responses.
It does not establish official accuracy, precision, recall, or improvement.
The reviewed references are themselves limited to the information in the
three local Kubernetes documentation records and the case wording.

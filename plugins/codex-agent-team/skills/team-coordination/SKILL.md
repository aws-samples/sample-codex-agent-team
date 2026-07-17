---
name: team-coordination
description: Use when the user requests parallel delegation, role specialization, a lead-member workflow, or coordinated subagent execution.
---

# Team Coordination

## Outcome

Run the smallest useful hybrid Codex team at the full width of genuinely
independent work. Maintain explicit ownership, file-disjoint writes, complete
handoffs, reliable liveness decisions, independent review, agent closure, and
main-thread consolidation.

Use this skill only when the user requests parallel delegation, role
specialization, a lead/member workflow, or coordinated agents. Multiple files
alone do not require a pool.

## Coordinator Position

The main thread is normally the coordinator. It owns requirements, design,
task partitioning, launches, steering, waits, decisions, result integration,
review orchestration, documentation close-out, and final status.

A spawned lead that cannot delegate should return a complete Spawn Plan to the
main thread. It must not quietly convert the workflow into a single-threaded
implementation.

Codex coordination is explicit:

- durable `.codex/specs/<slug>/` artifacts define requirements and task state
- spawn prompts define each worker's ownership and acceptance
- wait returns worker results
- steer corrects an active worker's scope or supplies a decision
- close terminates agents that are no longer needed
- current files, diffs, artifacts, and command output are ground truth

Do not assume an implicit shared task store or mechanically enforced claiming.

## Roles, Caps, And Names

| Role | Cap | Instance names | Owns |
| --- | ---: | --- | --- |
| `coding-agent` | 6 | `coding-1` through `coding-6` | Product code, tests, refactors, bounded fixes |
| `devops-agent` | 2 | `devops-1`, `devops-2` | IaC, CI/CD, containers, environment, runbooks |
| `review-agent` | 4 | `review-1` through `review-4` | One synthesizer plus optional analysts |
| `sa-agent` | 1 | `sa-1` | AWS architecture, security, reliability, performance, cost |

Every worker has a globally unique instance name within the run. Never launch
two active agents under the same identity.

Caps are ceilings, not quotas. Pool width equals the number of currently
claimable, file-disjoint tasks for that role, clamped to the cap. A future task,
blocked task, or same-file task does not justify another active worker.

Under-provision before over-provisioning. An idle pool adds stale messages,
duplicate effort, rate-limit pressure, and same-file race risk.

## Handoff Contract

Every spawn prompt includes:

- role agent and unique instance name
- objective and relevant repository context
- spec directory and exact task/wave reference
- exact file scope, writable files, and explicit no-edit boundary
- acceptance criteria and requirement/spec references
- produced/consumed interface contract
- dependencies and peer outputs
- verification command or concrete evidence
- expected output format
- warning that peers may edit nearby files concurrently
- whether the coordinator must wait for all named agents before consolidation
- approval boundaries for external, destructive, billable, or live actions

Example:

```text
Use `coding-agent` as `coding-2`.
Context: `.codex/specs/orders-api/`, Wave 2, order-handler task.
Scope: only `src/orders/handler.ts` and `src/orders/handler.test.ts`.
Acceptance: match `spec.md#order-interface`; reject invalid input using
`OrderError`; consume `OrderRepository` without changing its contract.
Run: `npm test -- orders/handler`.
Do not edit outside scope; peers are working concurrently.
Return instance, files changed, exact command outcomes, interface deviations,
blockers, docs changed, and residual risk.
The coordinator will wait for every Wave 2 worker before consolidation.
Do not deploy or write to external systems.
```

Reject an incomplete handoff before spawning. A worker should not have to infer
its files, interface, or definition of done.

## Launch

Before launch:

1. Confirm shared interfaces are stable enough for parallel work.
2. Confirm no two active tasks write the same file.
3. Determine intended width from claimable tasks.
4. Assign unique names and record ownership.
5. Identify which agents must all return before consolidation.

Spawn the intended pool concurrently using parallel tool calls. Do not launch
one independent worker, wait for it, then launch the next. A concurrent launch
reduces avoidable serialization and ensures every worker receives the same
current contracts.

If one spawn fails while others start, record the exact failed instance and
scope. Do not duplicate a successfully launched scope. Retry or replace only
the failed launch when evidence supports it.

## Monitor, Wait, And Consolidate

Keep the coordinator on coordination rather than implementation:

- answer interface questions
- make and log decisions
- steer scope drift promptly
- watch for newly unblocked downstream work
- preserve blockers and open gates
- avoid editing worker-owned files

Wait for all requested agents named in the wave before consolidation. A first
returned result is not permission to advance while peers are still active.
Collect results in batches when possible, then wait again for remaining agents.

For each result:

- verify the instance and assigned scope
- inspect current files and diff
- reconcile exact commands and outcomes
- record task status, blockers, decisions, and live-validation evidence
- identify interface changes affecting peers
- close the agent after its result is harvested and no follow-up is needed

If a requested result is missing, record the missing evidence and assurance
gap. Never fabricate or infer a worker's conclusion.

## Scaling

Scale up only when new tasks are:

- unblocked now
- independently understandable
- file-disjoint from every active writer
- covered by stable interfaces
- large enough to justify coordination overhead

Scale down when tasks converge on shared files, dependencies serialize work,
rate limits dominate, or remaining work is too small. Stop or close surplus
idle workers after preserving any useful result.

Do not keep a role at its cap merely because the cap exists. Do not spawn a
replacement while the original scope is still active.

## Quiet Agents, Stale Results, And Recovery

Silence is not failure. A quiet worker may be running tests, a plan, a build,
or a long review. Lack of a recent message, elapsed time alone, or lack of a
visible process is not positive evidence of death.

Before replacement:

1. Inspect current files, artifacts, and any partial result.
2. Check the agent's reported state through available lifecycle tools.
3. Wait for a bounded interval appropriate to the known command.
4. Steer the agent for a status/evidence update when useful.
5. Replace only with positive evidence: explicit failure, confirmed
   termination, corrupt/unusable output, or durable proof that acceptance
   cannot complete.

If recovery is justified, close the failed agent after harvesting partial
evidence, then respawn only the unfinished exact scope. Do not redo completed
work and do not take over broad implementation in the coordinator thread.

Treat late output from a replaced or closed worker as a stale result. Compare
it with current ownership and disk state before using it. Never apply stale
same-file changes over a replacement's newer work.

## Safety During Recovery

Recovery does not grant approval for destructive, billable, deploy, apply,
destroy, production, or external actions.

If a failed agent may have created live resources:

- stop colliding actors
- use read-only queries to establish state
- preserve authoritative backend/state locks and logs
- report resources that may still be live
- obtain explicit teardown authorization
- independently verify residue after approved cleanup

Never cross a held safety gate because its owner became quiet.

## Review Coordination

For a cohesive scope, use one `review-agent` as synthesizer. For independent
slices:

- `review-1` is synthesizer and sole author of `review.md`
- `review-2` through `review-4` are analysts
- analysts write no review file
- the synthesizer waits for every requested analyst or records missing evidence
- the synthesizer checks cross-slice contracts and emits one verdict

Count every synthesizer spawn for the whole team run. Initial review, targeted
re-review, replacement, and interrupted retry share one non-resetting maximum
of three cycles.

Only cycle 1 or 2 FAIL may produce a scoped fix wave. Cycle 3 is terminal. On
cycle 3 non-PASS, stop fixes/reviews, close active agents, preserve evidence,
and report blocked. Never spawn cycle 4.

## Steering, Stop, And Close

Use steer to:

- clarify a contract
- communicate an approved decision
- correct scope drift
- request missing verification or output
- tell a worker to stop before an unsafe boundary

Do not steer a worker into a materially broader file scope; issue a new
handoff after updating artifacts.

Use close after:

- a completed result has been harvested
- a failed/replaced worker's partial evidence is preserved
- an idle worker is no longer needed
- cycle 3 terminates the run

Before final response, perform an active-worker check. Confirm every requested
result is harvested or blocked, every no-longer-needed agent is closed, and no
agent remains active on required work.

## Degraded Workflow

If required agent capability is unavailable:

1. State the exact unavailable capability or failed call.
2. Explain the lost assurance: parallelism, role specialization, independent
   review, or isolation.
3. Preserve the Spawn Plan and durable tasks.
4. Obtain explicit user approval before single-threaded degraded execution.
5. Label any self-review as pending independent review, never PASS.

Do not present degradation as equivalent to the requested team workflow.

## Coordinator Completion

Return artifact paths, worker outcomes, missing results, task/decision status,
review cycle/verdict, exact verification, open live-validation gates,
documentation status, closure status, and residual risks.

Completion requires a final active-worker check and no required worker still
active. A blocked cycle-3 run closes agents and reports the unresolved evidence
instead of continuing automatically.

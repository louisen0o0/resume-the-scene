# v0.3 Cold-start Canary 2

Date: 2026-09-18
Source: user-provided fan-in from a fresh Grok Bot cold-start run
Result: PASS

## Test shape

The worker received only:

- project root: `/Volumes/SaLa/08_界外/B30-V1-恢复现场吧`
- a read-only request to recover current task, completed work, trusted evidence, active decisions, and exact next action.

It did not receive prior chat history, file names, command names, v0.3 implementation details, or the previous Canary result.

## Observed recovery

The worker independently recovered:

- current task: `#t0`, goal `#g0`
- current exact action: `#a6 = run_coldstart_canary_2`
- skip/done: E001-E011
- selected trusted evidence: project RSM state + E001-E011
- active decision: `#d_v03_scope`
- decision choice: `thin_core_usability_expansion`
- exact continuation point: `#a6`

The worker used the repository's own handoff surface and reported that CURRENT / PROJECT / memory / decision / evidence were aligned.

## Mutation check

PASS.

The worker reported no file writes, no checkpoint mutation, and no git mutation.

## Interpretation

This run closes the specific usability gaps exposed by Canary 1:

- active decision is explicit instead of inferred;
- the next action is explicit;
- project version / state are aligned;
- the worker can recover the handoff without chat history.

No new core protocol concept is justified by this run.

## Residual scope

External publication is still gated.

The next project action should be release-candidate preparation and final local audit, not another speculative protocol expansion.

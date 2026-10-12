# Research discussion, 13 October 2026

## 1. Towards Stable Temporal Acceleration of Frozen Action-Chunk Policies

Current empirical evidence and mechanism-identification plan.

The stability plug-in is a research target, not a validated method.

## 2. Deployment-time acceleration

Can frozen policies execute faster without losing reliability?

An existing temporal accelerator shortens execution of a predicted chunk. We aim to identify failures and eventually apply minimal execution correction while retaining actual speed gains.

## 3. Current execution pipeline

Observation → frozen π0.5 → 10-action chunk → runtime retime → execution.

No policy fine-tuning in the comparison. Current protocols also change query cadence.

## 4. Aggregate speed–reliability observations

| Setting | SR (%) | Successful mean time (s) | Paired median speedup | Successful mean policy calls |
| --- | ---: | ---: | ---: | ---: |
| RT-1.0 | 97.90 | 7.43 | 1.00× | 15.29 |
| RT-1.5 | 95.45 | 5.76 | 1.33× | 19.61 |
| RT-2.0 | 80.50 | 5.57 | 1.47× | 22.71 |
| RT-2.5 | 60.70 | 5.73 | 1.54× | 29.04 |
| RT-3.0 | 48.85 | 5.55 | 1.53× | 37.34 |

Supplied verified overall table only. Requested acceleration and achieved speedup differ. Completion-time and call means condition on success. Document exact paired eligibility before inferential interpretation. Uncertainty has not been supplied.

## 5. Exploratory RT3 diagnostic associations

First 100 control steps, or 5 seconds, per episode. RT3 failure N=31, success N=19.

| Median proxy | Failure | Success |
| --- | ---: | ---: |
| Query-boundary translation direction change | 0.1793 | 0.1061 |
| Requested translation bound-excess step fraction | 0.64 | 0.63 |
| EEF path efficiency | 0.7469 | 0.8368 |

Task-level counterexamples exist. These associations establish neither causality nor a universal instability signal.

## 6. Four competing hypotheses

- H1: Motion realization distortion.
- H2: Cross-query commitment instability.
- H3: Interaction completion mismatch.
- H4: Object-state deviation and failed recovery.

No winner yet. Mechanisms may coexist.

## 7. Identification problem

RT1: speed 1×, query every 10 control steps.

RT3: speed 3×, query every 3 control steps.

The comparison changes acceleration and query cadence together.

## 8. Controlled protocol comparison

- S1-Q10 executes the raw 10-step prefix.
- S1-Q3 executes raw actions a0, a1, a2 and queries again, without retiming.
- S3-Q3 executes three compressed actions and queries again.

S1-Q10 versus S1-Q3 tests cadence and prefix-execution effects. S1-Q3 versus S3-Q3 tests compression at matched query cadence. Neither contrast eliminates every downstream execution difference.

Task4 is a falsification-oriented choice because its direction proxy reverses the aggregate pattern. Use 20 fixed, outcome-independent init states. Proposed collection remains a plan until execution and artifact counts are verified.

## 9. Synchronized execution diagnostics

Action/source mapping → controller physical goal → robot/EEF/gripper → object pose/contact → task predicates.

Log task, init, repeat, seed, control step, simulation time, query id and local action index. Preserve raw and executed chunks, exact sent actions, controller goals, robot state, movable-object state, contact pairs and task progress. Synchronize agentview and wrist videos explicitly to control steps.

Simulator ground truth diagnoses mechanisms. It does not imply that a deployable plug-in uses privileged state.

## 10. Future stability plug-in and meeting questions

Existing accelerator → proposed monitor/corrector → robot, with execution feedback.

Monitor and corrector remain mechanism-dependent and under investigation.

1. Is execution instability a sufficiently focused research problem?
2. What remains confounded in the S1-Q3 control?
3. Which deployment signal can support minimal correction?

The project is ongoing and welcomes collaborators.

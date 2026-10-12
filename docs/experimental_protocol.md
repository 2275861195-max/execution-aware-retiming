# Matched-rollout experimental protocol

Status: planned diagnostic protocol under active validation. This document defines what should be measured, not a completed experiment report.

The current amendment is the [three-condition control plan](next_experiments.md). RT1/RT3 also change query cadence; a two-condition comparison cannot attribute outcomes to compression alone. The [current evidence summary](current_evidence.md) distinguishes released aggregate observations from planned tests.

## Frozen-policy principle

Keep policy parameters, checkpoint, observation processing, action normalization, controller implementation, control frequency, simulator time step, and success predicate fixed. The diagnostic treatment is the retiming rule. Do not retrain the policy or modify controller bounds during mechanism diagnosis. Read-only instrumentation must not silently alter execution.

## Matched comparisons

Pair RT-1.0 reference execution with accelerated execution on the same task and saved initialization. Record task identifier, environment and source versions, checkpoint identifier, initial-state hash, seed, action representation, retiming factor, chunk horizon, commitment length, and policy query schedule. A common seed alone does not ensure identical initial state; validate the restored state.

Pairing controls initialization, not later trajectories: after divergence, observations and future policy predictions may differ. Distinguish closed-loop deployment comparisons from fixed-chunk replay diagnostics. Replay can isolate execution of a source chunk but does not reproduce ordinary closed-loop performance.

## Required synchronized records

| Record | Purpose |
| --- | --- |
| Video and frame timestamps | Visualize interaction order and first divergence |
| Measured EEF pose and object state when available | Quantify motion and physical interaction |
| Raw source chunk and policy query time | Preserve the policy prediction before retiming |
| Source coordinate and retimed commands | Reconstruct the scheduled action clock |
| Effective commands after normalization, clipping, and scaling | Separate intended reference from controller input |
| Gripper commands, aperture, and contact/readiness indicators | Inspect grasp and release transitions |
| Termination reason and success predicate | Separate success, failure, timeout, and runtime error |
| Control ticks, simulated time, inference time, and wall time | Prevent nominal acceleration from being mistaken for useful speedup |

Log the actual command processing order. If an internal quantity cannot be measured, label it unavailable rather than substituting an unverified proxy. Check timestamp alignment and instrumentation overhead.

## Video organization and labeling

Keep videos in a dedicated artifact store, separate from source code. Use a manifest linking pair ID, task, initialization, retiming condition, seed, outcome, and video filename. Suggested naming: `task__pair-id__condition__success.mp4`, with `failure`, `timeout`, or `error` as other outcome labels. Labels must derive from the environment success predicate and termination record, not visual guessing. Preserve both successful and failed episodes. Raw videos remain private until curated and cleared for release.

## First-divergence analysis

1. Verify that both episodes start from the matched state.
2. Align by control time and source coordinate; these answer different questions and must not be conflated.
3. Identify the first meaningful command, tracking, object-state, or interaction discrepancy using predefined tolerances.
4. Inspect the interval before that discrepancy, including saturation, chunk refresh, and gripper events.
5. Annotate phenotype, alternative explanations, evidence, and uncertainty.
6. Test whether the proposed deficit precedes the harmful transition, and look for counterexamples where a deficit does not cause failure.

Video review is a localization tool, not sufficient causal evidence. Annotators should avoid inferring hidden contact states from appearance alone.

## Budgets and efficiency

Keep the official task success definition fixed. Explicitly state whether episode limits are measured in control ticks, simulated time, or wall time, and report each. Do not count an early failed termination as acceleration. Report success across all matched initializations and time-to-success separately, with uncertainty and the number of independent pairs once results are validated. Avoid selecting only successful accelerated episodes.

## Diagnostic sequence

Start with reference and accelerated closed-loop pairs. Next inspect command and tracking records. Where justified, add separately labeled fixed-chunk replay and representation-aware diagnostics. Controller-changing interventions belong to a later, separate experiment with an explicit protocol amendment; they must not be mixed into the baseline diagnosis.

## Reproducibility and release criteria

Before publishing conclusions, validate outcome labels, missing records, pair completeness, version pinning, action semantics, clock alignment, and confounds. Release reproducible configuration and curated summaries only after review. Do not hard-code unpublished result numbers into this protocol. Store failures and negative evidence as well as illustrative cases.

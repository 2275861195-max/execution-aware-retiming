# Research roadmap

The project is ongoing and seeking collaborators. These stages are evidence-gated plans, not completed milestones or guaranteed deliverables.

## Stage 1 — Characterize accelerated execution

Establish matched reference and accelerated rollouts with a frozen checkpoint. Validate command semantics, initialization matching, outcome labels, synchronized video, and EEF logging. Locate first divergences and build a failure phenotype taxonomy.

**Exit criterion:** trustworthy diagnostic records and a clear distinction between nominal compression, physical execution time, and task success.

## Stage 2 — Identify failure mechanisms

Distinguish displacement deficit, tracking limitations, contact dynamics, gripper timing, distribution shift, replanning inconsistency, and timeout effects. Seek both supporting evidence and counterexamples. Separate closed-loop deployment behavior from fixed-chunk replay diagnostics.

**Exit criterion:** a bounded, evidence-supported mechanism claim that survives plausible alternative explanations; otherwise revise the hypothesis.

## Stage 3 — Develop execution-aware acceleration

Use the diagnostic evidence to design a provisional retimer. Candidate ideas include constraint-aware clock advancement and interaction-readiness-aware scheduling. Compare with simple retiming and commitment-length baselines under matched settings. Account for sensing and decision overhead. Keep training-free claims conditional on genuinely frozen policy weights.

**Exit criterion:** reproducible implementation, explicit assumptions, and ablations showing which component provides useful task-level acceleration.

## Stage 4 — Long-horizon robustness and cross-policy generalization

Evaluate held-out initializations, varied manipulation transitions, long-horizon tasks, and additional compatible frozen policies. Measure robustness to imperfect progress signals and changed execution conditions. Report failure modes, uncertainty, and generalization limits rather than a single aggregate score.

**Exit criterion:** validated public evaluation with configuration, provenance, and appropriately scoped conclusions.

## Collaboration opportunities

We welcome collaboration on robot controller semantics, contact-rich execution, progress estimation, temporal planning, rollout instrumentation, video annotation, and reproducible evaluation. Start with a focused GitHub issue describing your interests. New ideas are welcome, including evidence against the current hypothesis.

## Release policy

Publish protocol and framing now; release implementation progressively after stabilization; publish curated evidence and summaries after validation. Raw experimental records and checkpoints are not part of this showcase. No publication acceptance or performance improvement is claimed.

# Experiments and public summaries

Experimental results are currently private and under active validation. No numerical performance claim is made in this directory. It will later contain reproducible experiment configurations, version manifests, curated public summaries, and references to approved visual evidence.

## Planned public contents

- Matched RT-1.0 versus accelerated rollout configurations.
- Task and initialization manifests without private infrastructure details.
- Policy checkpoint identifiers and environment/controller provenance.
- Validated outcome summaries with uncertainty and clear termination categories.
- First-divergence annotations, competing explanations, counterexamples, and negative results.
- Method ablations once an execution-aware retimer is sufficiently stable.

## Artifact boundary

Raw videos, simulator records, datasets, and checkpoints stay in a separate private artifact store during validation. Public summaries will link only to reviewed artifacts cleared for release. Success/failure labels must come from the environment predicate and termination records. Missing data and runtime errors must remain distinct from task failure.

Frozen-VLA retiming diagnostics on LIBERO are separate from ACT/DP training in RoboBase / BiGym. Results from the latter will not be used as evidence for this project without an explicitly defined, separate study.

See [the protocol](../docs/experimental_protocol.md) for the diagnostic design and [the roadmap](../docs/roadmap.md) for release gates. Researchers interested in evaluation or annotation are welcome to open an issue.

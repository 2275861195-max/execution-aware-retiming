# Research question

Can frozen action-chunk policies execute substantially faster at deployment time without sacrificing reliability?

We study an existing temporal accelerator followed, potentially, by a lightweight execution-stability layer. The accelerator itself is not necessarily the contribution. The proposed plug-in should make minimal corrections and retain **measured** speed gains; its signals and algorithm depend on mechanism identification.

Four competing explanations remain open:

1. **H1 — Motion realization / execution distortion:** accelerated commands may not be physically realized as intended.
2. **H2 — Cross-query commitment instability:** changed replanning cadence may destabilize continuous or discrete intent.
3. **H3 — Interaction completion mismatch:** robot motion may advance before grasp, contact or placement completes.
4. **H4 — Object-state deviation / failed recovery:** interaction perturbs object state, followed by inconsistent predictions or failed recovery.

These are neither mutually exclusive nor established conclusions. No universal instability detector, novelty claim, or policy-independence claim follows from the current data.

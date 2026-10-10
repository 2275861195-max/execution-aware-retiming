# Research notes: clock, commands, and physical progress

This document develops a diagnostic formulation, not a proven explanation or final algorithm.

## Evidence labels

**CONFIRMED OBSERVATION:** The public record currently establishes the research scope and protocol, not a validated empirical mechanism. Mathematical statements below are conditional properties of the specified representation, not robot measurements. Empirical observations will be added with artifact identifiers after validation.

**WORKING HYPOTHESIS:** Accelerated scheduled progress can outrun realizable interaction progress, making a subsequent phase premature.

**OPEN QUESTION:** Which mechanism dominates each failure, and can an execution-aware clock improve task-level efficiency without reducing success?

## Action chunk and cumulative trajectory

For incremental translations $a_i\in\mathbb{R}^3$ expressed in a common coordinate system and unit, define

$$Q(0)=0,\qquad Q(j)=\sum_{i=0}^{j-1}a_i.$$

Interpolate $Q$ between integer indices. Let $\phi_t$ be the source coordinate scheduled at control tick $t$. A displacement-preserving retimed reference is

$$\widetilde a_t=Q(\phi_{t+1})-Q(\phi_t).$$

For a source interval with matching endpoints, summing these commands telescopes to the same reference displacement. It does not preserve intermediate contacts, elapsed physical time, or the actually executed trajectory. Normalized commands must first be interpreted through the controller scaling. Rotations require an appropriate manifold-aware construction; gripper commands require event semantics. Blind summation of every action component is not justified.

## Clock-indexed source coordinate

Reference execution advances approximately one source index per tick; a fixed accelerated clock may use $\phi_{t+1}=\min(H,\phi_t+\rho)$ with $\rho>1$. This is a nominal source-clock acceleration, not a measured wall-clock speedup. Replanning, inference, rendering, and evaluation overheads must be accounted for separately. Chunk boundaries and the policy query schedule must be logged because they change the meaning of the clock.

## Controller clipping and realization

A simplified componentwise bound gives

$$u_t=\operatorname{clip}(\widetilde a_t,-b,b).$$

In general, $\sum_t u_t\neq\sum_t\widetilde a_t$. This arithmetic fact motivates measuring effective commands; it does not prove that clipping explains a failed episode. Real controllers may additionally scale actions, use absolute targets, impose rate limits, or integrate a closed-loop tracking law. The simulator state evolves under dynamics and contact, not a simple sum of commands. Record the true processing order and units before interpreting residuals.

## Scheduled versus realized progress

Scheduled progress can be represented by a normalized source coordinate $p_s(t)=\phi_t/H$. Realized progress $p_r(t)$ is task-dependent and must be operationalized rather than assumed. A path projection can be ambiguous when trajectories self-intersect, and proximity alone does not certify a grasp or successful placement. Interaction milestones may be more meaningful than a single continuous scalar.

A proposed execution-progress gap is

$$g(t)=p_s(t)-p_r(t),$$

only when the two quantities share a valid scale. Otherwise report event-specific readiness deficits or physical tracking errors instead. Do not subtract unlike quantities or label ordinary tracking lag a task-progress deficit without evidence.

## Why long-horizon manipulation?

Long-horizon tasks contain ordered prerequisites: approach before grasp, stable grasp before lift, alignment before contact, support before release. Small earlier errors can accumulate or become consequential at a later transition. This makes first-divergence analysis useful, but also makes causal attribution harder: an observed late failure may originate much earlier.

## Competing explanations and discriminating measurements

| Explanation | Relevant evidence | What would weaken it? |
| --- | --- | --- |
| Displacement deficit | Integrated reference, effective command, and measured EEF motion | Failure despite comparable realized displacement |
| Tracking limitation | Timestamped reference and measured pose, lag and overshoot | No tracking divergence before failure |
| Interaction timing | Grasp/contact/support events around phase transitions | Physical prerequisites achieved before the transition |
| Gripper semantics | Gripper command, aperture, object motion | Equivalent closure/release timing and state |
| Distribution shift | Observations and subsequent policy chunks | Failure already present with a fixed diagnostic chunk |
| Replanning inconsistency | Chunk boundary discontinuities and query schedule | Failure within a chunk before refresh |
| Timeout / bookkeeping | Control ticks, simulated time, wall time, termination reason | Same outcome under a correctly matched budget |

These are alternative or interacting mechanisms. Temporal association is not causal identification. Negative evidence, counterexamples, and unsuccessful diagnostics should be retained.

## Method questions

Could a retimer slow the source clock near interaction boundaries? Could tracking residuals detect insufficient realization? How much overhead would sensing or readiness estimation add? Would adapting the clock create new distribution shift or replanning instability? These questions guide future methods only after the diagnostic evidence is credible.

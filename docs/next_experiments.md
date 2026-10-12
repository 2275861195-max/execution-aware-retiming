# Next diagnostic experiment — proposed, not completed

Current RT1 and RT3 differ in both temporal compression and query cadence. Use a controlled three-condition comparison:

| Condition | Requested speed | Query interval | Execution |
|---|---:|---:|---|
| S1-Q10 | 1× | 10 control steps | Raw ten-action prefix |
| S1-Q3 | 1× | 3 control steps | Raw a0, a1, a2; re-query; no retiming |
| S3-Q3 | 3× | 3 control steps | Current temporally compressed execution |

S1-Q10 versus S1-Q3 tests cadence/prefix-execution effects, including changed feedback opportunities. It does **not** isolate query frequency alone. S1-Q3 versus S3-Q3 tests temporal compression at matched cadence; source-time coverage and downstream controller/contact effects still differ.

Start with task4 because it provides a counterexample to the direction proxy, not because it produces the cleanest signal. Preselect 20 fixed, outcome-independent initial states. The meeting plan is 6 interface smoke episodes, then 60 paired diagnostic episodes; a second 40-episode repeat of the two Q3 conditions may estimate stochastic variability. Collection status must be checked separately before reporting results.

Hold policy checkpoint, software revision, initial state, seed schedule, controller, horizon, termination rule and success predicate fixed. Record deviations. Seed matching is not a guarantee of identical trajectories. Report per-condition outcomes and paired differences with uncertainty before making mechanism claims.

## Required synchronized instrumentation

Record task/init/repeat/seed, step and simulation time, query ID and local action index; raw chunks, retimed chunks, source-time mapping and exact env actions; scaled controller delta and position/orientation goals where accessible; EEF poses, joint position/velocity, gripper commands and physical motion; movable-object poses and velocities; finger-object, robot-object, support and receptacle contacts; per-step predicates, reward, done and final success.

Save agentview and wrist video with explicit frame-to-step synchronization. Simulator object/contact/predicate state is **diagnostic ground truth**, not an assumed input to a deployable plug-in. Log unavailable fields explicitly rather than inventing values.

Do not overwrite training sources or checkpoints to implement evaluation instrumentation. Keep policy/environment compatibility audits separate from retiming claims.

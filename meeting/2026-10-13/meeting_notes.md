# Discussion notes

## 30-second pitch

We accelerate the execution of a frozen action-chunk policy after prediction. Mild acceleration retains high reliability, but at higher requested speeds success falls while measured speed gains saturate. We are investigating which execution mechanism fails, separating temporal compression from replanning cadence and recording robot–object interactions. Our longer-term goal is a lightweight stability layer that preserves useful speed gains without retraining the policy.

## Two-minute project explanation

Our starting point is a frozen π0.5 policy that predicts action chunks. We apply runtime temporal acceleration to those predictions rather than retraining the policy. The supplied aggregate results show that 1.5× requested acceleration achieves 95.45% success with 1.33× paired median speedup. At 3× requested acceleration, success falls to 48.85%, while paired speedup reaches only 1.53×. Requested speed therefore overstates the speed gain that successful execution actually achieves.

We want to understand what goes wrong before designing a correction. In a smaller diagnostic batch, direction changes and EEF path inefficiency show aggregate associations with failure, but individual tasks reverse those patterns. Requested action bound excess is nearly the same for successes and failures. These measurements cannot yet identify a causal failure mechanism.

We currently consider four explanations: motion does not realize the requested command, frequent replanning changes commitment, physical interaction has not completed when the action advances, or object perturbation undermines subsequent recovery. The existing RT1 and RT3 protocols change both temporal acceleration and query cadence. A raw three-action-prefix control provides a useful comparison, although it also changes prefix execution and feedback opportunities.

Our next experiment uses fixed task4 init states and synchronized action, controller, robot, object, contact and task-predicate logs, with two camera views. Task4 deliberately challenges an aggregate proxy instead of showcasing the cleanest signal. Once a mechanism survives controlled tests, we can investigate a minimal post-acceleration monitor and corrector. Simulator state serves diagnosis, while a deployable layer must rely on available observations. The method and cross-policy generalization remain research goals, and we welcome feedback on the controls and suitable deployment signals.

## Strongest evidence, main uncertainty and next experiment

The strongest current evidence is the supplied overall speed–reliability tradeoff, especially the small increase in measured speedup between RT2 and RT3 despite the large success-rate decline.

The main uncertainty is the failure mechanism. Temporal compression and query cadence currently vary together, and exploratory proxies have task-level counterexamples.

The next experiment compares S1-Q10, S1-Q3 and S3-Q3 on 20 fixed task4 init states, with Q3 repeats where practical and synchronized physical diagnostics. This remains a proposed experiment until artifacts confirm completed execution.

## Evidence boundary

The supplied overall tradeoff is the quantitative starting point. Do not use the older suite-level table while its provenance remains under audit. No new completed experiment or implemented stability method is claimed here.

Means of completion time and policy calls use successful episodes, so their population changes with requested speed. The exact pairing rule, eligible sample count, treatment of failures and suite aggregation must accompany the speedup statistic. The supplied summary does not provide uncertainty estimates.

## Diagnostic interpretation

The 100-episode audit contains 50 RT3 episodes, comprising 31 failures and 19 successes. Each proxy uses the first 100 control steps. Requested bound excess is nearly equal between groups and does not establish actual controller saturation.

The direction-change association reverses for task4: failure 0.1793, success 0.2386. The efficiency association reverses for task8: failure 0.8551, success 0.8329. Task mix and diagnostic selection can therefore drive aggregate differences. Object state, contacts and task predicates are missing from the earlier diagnostic traces.

## Experimental interpretation

The S1-Q3 control is useful but changes executed prefix length and opportunities for closed-loop correction as well as query cadence. S1-Q3 versus S3-Q3 holds cadence fixed while changing temporal compression, source-time coverage and downstream controller interaction. Frame this as a controlled protocol comparison, not complete causal isolation.

Use fixed init states chosen independently of the diagnostic outcomes. Repeat policy sampling conditions where practical. Log initialization hashes and the actual random-number scheme. Matched init and seed alone do not prove identical trajectories.

The original meeting brief proposes six smoke episodes followed by 60 episodes and optional Q3 repeats. Later operational planning may collect 100 episodes including repeats. Keep the repository status separate from this plan and update completed counts only after verifying records, traces and videos.

## Deployment scope

The current empirical evidence uses frozen π0.5. Policy independence, ACT/DP generalization and canonical BiGym compatibility remain future validation. A controller semantic change can alter the checkpoint/environment pair, so do not label an unverified evaluation as a strict official reproduction.

Simulator contacts and predicates are diagnostic ground truth. A future deployable monitor needs signals available at deployment, which may require observable proxies or estimators.

## Questions for collaborators

- Which hypothesis predicts a specific, observable failure ordering?
- Can a localized intervention distinguish H1–H4 without hiding failure through slower execution?
- What actual-speed metric and failure penalty should define the objective?
- What minimal observation can support a deployable correction?
- Which task should falsify an apparently strong aggregate signal?

## Source

Author-supplied research meeting brief and verified aggregate values, 12 October 2026. This discussion deck summarizes supplied observations without asserting independent validation of raw records.

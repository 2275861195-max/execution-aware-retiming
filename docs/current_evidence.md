# Current evidence and limitations

Updated for the 13 October 2026 research discussion. The two public CSVs transcribe the author-supplied verified aggregate summary; this repository update does not constitute a fresh audit of the private episode-level files.

## Observed tradeoff

[Overall data](../data/aggregated/overall_tradeoff.csv) show that RT-1.5 retains 95.45% success at 1.33× paired median speedup. Moving from requested 2× to 3× reduces success from 80.50% to 48.85%, while measured paired median speedup moves only from 1.47× to 1.53×.

Completion time and policy-call means are **success-conditioned**. Paired median speedup uses eligible paired episodes; the exact eligibility rule and denominator must accompany an episode-level release. No confidence intervals have been calculated here. Requested acceleration is not achieved speedup, and successful-episode timing alone does not measure the total cost of failures.

The older suite-level table is excluded while its provenance remains under audit. These results concern the current frozen π0.5 setup, not an established policy-independent method or a canonical ACT/DP reproduction.

## Exploratory diagnostic subset

The prior 100-episode diagnostic batch is separate from the formal aggregate study. Its RT3 subset contains 31 failures and 19 successes. All listed metrics use the first 100 control steps (5 seconds), not whole episodes. The selected tasks are not a representative sample of all tasks.

| Median proxy | Failure | Success |
|---|---:|---:|
| Query-boundary translation direction change | 0.1793 | 0.1061 |
| Requested translation bound-excess step fraction | 0.64 | 0.63 |
| EEF path efficiency | 0.7469 | 0.8368 |

Task4 reverses the direction-change pattern (failure 0.1793, success 0.2386). Task8 reverses the efficiency pattern (failure 0.8551, success 0.8329). Task-level group counts are not supplied and are left blank in the CSV.

These are associations, not causes or validated early-warning signals. Global bound excess is similar between outcomes. Object state, contacts and task predicates are missing from this older diagnostic trace. Causal ordering is unknown.

## Evidence levels

- **Observed:** supplied aggregate speed–reliability tradeoff.
- **Exploratory:** selected-task motion proxies and counterexamples.
- **Hypotheses:** H1–H4, with no winner selected.
- **Proposed:** controlled diagnostic comparisons and a future stability plug-in.

No new diagnostic batch is represented as completed by this update. ACT/DP BiGym training-time source and floating-base semantics remain a separate compatibility/provenance question.

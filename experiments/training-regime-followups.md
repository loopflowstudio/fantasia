# Follow-up mechanism protocols

2026-10-04. These proposals belong to ETU-91's experiment design; no execution
or expensive allocation is authorized by their presence. Each requires frozen
inputs and predictions, a separately approved cost cap, fresh evaluation deals,
and retained failed attempts before scoring. None is a runnable regime stage.

## Following the learned policy into search and belief experiments

Search remains a product capability, including belief-conditioned advice.
Policy-only evaluation isolates the source of learned strength; it is not a
decision to remove search from Etude. Deliver the following concrete follow-up
experiment specifications with prerequisites, artifact contracts and proposed
analysis, while keeping their unimplemented stages out of runnable recipes:

1. **Compound combat decisions:** integrate a trainable autoregressive decoder
   over complete legal declarations. Sum conditional log probabilities for
   the joint action; define reward/discount/value boundaries explicitly and
   forbid grouping across intervening information or opponent decisions.
   Compare sequential and grouped policies on the same game outcomes and
   wall budget; report equivalent underlying choices so collapsed prompts
   cannot manufacture throughput gains. Adapter parity alone is insufficient.
2. **Search after RL:** freeze each selected raw/EMA policy identity. On a
   tractable pool, obtain exact posterior weights from that same frozen
   behavior policy, sample compatible worlds, roll out with viewer-safe
   policy observations, evaluate leaves and take one local regularized update.
   Compare policy-only, uniform-belief search and exact-belief search at matched
   elapsed decision budgets. Never feed full sampled worlds into the policy.
   Exact ranges fitted to another population do not establish update equivalence.
3. **Distill the local update:** retain base policy, action-value estimates,
   belief/rollout policy identities, reference, step size and computed target
   distribution. Compare hard argmax targets and regularized soft targets from
   the same roots/cost. Old per-action scores without those identities cannot
   reconstruct this target. Measure student strength, policy mixing and
   adversarial response; soft targets alone do not guarantee sound bluffing.
4. **Amortized beliefs:** collect frozen-policy self-play with hidden truth as
   labels only. Train a constrained autoregressive sampler; keep whole games
   separate across train/validation/test. Compare calibration, legal support,
   sampling cost and resulting search strength against exact beliefs on a
   tractable pool before widening the pool. All widening is a new world-bound
   comparison, not an unverified ten-million-hand extrapolation.

Add a frozen-opponent exploiter protocol for both main arms: independent
attacker seeds, terminal rewards, equal attacker budgets increasing at declared
checkpoints, and fresh final deals. Plot attack success versus attacker compute.
An unsuccessful bounded attacker is not an exploitability certificate.
Charge attacks and their evaluations explicitly; they are outside the proposed
168-hour comparison unless its allocation is amended. Reuse the repaired
`NetOpponentTrainer` frozen-opponent mode, not a second training implementation.
Run S1-S5 at policy checkpoints after verifying current-world legality and
intended strategic premises; report unsupported scenarios rather than silently
substituting old scores. Behavioral failures qualify arena gains.

The document freezes seeds, budgets, numeric prediction (proposed B=.55),
kill criteria and strongest confound before costly runs via `lf commit`.
Training, validation, development and final deal families are disjoint.
The strongest confound is recipe maturity: a negative result may reflect
untuned self-play treatments, not a limit of direct RL.


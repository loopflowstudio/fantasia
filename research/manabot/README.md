# manabot: the questions that matter

**2026-10-09 · MTG-130 · agent-written draft for Jack Heart's review.**
This is a research snapshot, not live experiment status or permission to run work.
Start here; [the experiment register](experiments.md) retains negative, incomplete
and operational evidence as well as successes. [Confidence](confidence.md) separates
working software from effective learning. [Draft findings](findings.md) cite the
experiments, not project completion.

The immediate objective is a reproducibly trained Allies/Lessons challenger, not
an unrestricted claim about Magic. **We have stronger evidence that the machinery
works than that the current recipe keeps producing stronger players.** The latest
reported baseline gain is important but still pending committed final analysis in
this snapshot. A flat greedy score is not yet a diagnosed learning ceiling.

## Five priority questions

Ranking is a proposed order of decision value, not an approved experiment queue.
Child questions and exact area ownership are in [the hierarchy](questions.md).
Experiments link to questions, never directly to areas; an experiment can inform
several questions. Links below give the prominent evidence; each question's
complete attachment list is in the register, including historical systems work.

### 1. Are we measuring stronger play, or just getting better at greedy?

`trustworthy-evaluation@1` · **Evaluation**

**Why now:** almost every recent score uses scripted greedy. A misleading yardstick
would invalidate the apparent plateau, capacity ranking and curriculum decisions.

**Known:** deal/seat pairing, exact replay and artifact admission have concrete
software evidence ([arena instrument](experiments.md#allies-lessons-arena),
[pooling factorial](experiments.md#pooling-filter-followup)). Historical
[exp-06](experiments.md#exp-06-newworld-training) exposed a single-deal evaluation
bug; [exp-09](experiments.md#exp-09-control-competency) showed strong aggregate
search play coexisting with poor delayed-control decisions. Neither establishes a
current checkpoint's competence. No current human-challenger or exploitability
criterion is met by these reports.

**Pending:** [head-to-head](experiments.md#head-to-head) fixes ten entrants and
25 pairings, 400 games each; no results. Its learned entrants are mostly single
seeds, and the 26k/63k/100k checkpoints are one lineage, not three training
replicates. [MTG-118 final evaluation](experiments.md#current-baseline) reportedly
shows a three-seed held-out greedy gain; it does not test general strength.

**Would settle the next decision:** the frozen head-to-head contrasts can reveal
whether greedy misses ordering among these artifacts. Replicated method claims
then need independent seeds, held-out paired deals, a retained payoff matrix,
matched inference cost, and selected-world tactical or adversarial checks.
Human performance needs its own predeclared cohort. An Elo score alone is not enough.

### 2. What limits continued learning: update selection, schedules, or exploration?

`continued-learning@1` · **Optimization**

**Why now:** the long GPU lineage and rate-restart attempt raise different possible
failure mechanisms. We should not spend another long run treating them as one.

**Known:** [pooling × floor](experiments.md#pooling-filter-followup) directly removed
the floor in a three-seed, 600-update screen: more token exposures, no demonstrated
strength benefit. [Actor-only filtering](experiments.md#ataraxos-technique-screen)
at 1,240 updates gave +3.33 [−4.33, +11.33] points at 1.45× training time across
three seeds; it remains unpromoted. These are **early**, not late-training tests.
[History diagnostics](experiments.md#history-results) measured 35 empty-filter
updates and showed that logged entropy described only the last optimized minibatch.
[Numerical repair](experiments.md#numerical-health) proves an underflow mechanism,
not the historical cause of the failed GPU batch or restoration of exploration.

**Pending, not conclusions:** [restart](experiments.md#restart-learning-rate) was
reported disk-stopped near 6.7k/12k updates in its first seed; the reported 3e-4
collapse and zero selected advantages are not an isolated floor intervention.
It also resets Adam/EMA and collection streams. [Early LR](experiments.md#early-learning-rate)
tests only the first 1,500 updates. Reported MTG-118 improvement to 10k is a reason
**not** to assert that longer training universally stops helping.

**Would settle the next decision:** establish the plateau at shared checkpoints
and common cost first, then compare continuation from the same frozen parent with
optimizer state and schedule clocks controlled. Measure support by decision type,
retained actor/critic samples, zero-update counts and actual parameter movement.
A late floor intervention, LR change and regularizer change must remain distinct.
No retained experiment here isolates late tau decay or exploration collapse.

### 3. What representation and model size buy useful strength per unit cost?

`model-fit@1` · **Architecture**

**Why now:** the GPU comparison jumps from width64/depth2 to width384/depth8;
size, exposure, inference cost and training endpoints differ. It cannot nominate a
capacity winner by endpoint score alone.

**Known:** [value aggregation](experiments.md#value-token-screen) (three seeds,
800 updates, 1,800 replayed games) leaves masked mean and value token unresolved.
The [history continuation](experiments.md#history-results) has an endpoint effect
of 0 [−11, +9.33] points over three seeds and 1,200 development games, without
initialization scores. More information has not demonstrated a benefit there.
[Structural katas](experiments.md#w2-214-structural-semantic-katas) rule out specific
encoders, not the current policy's ability to play combat. Tiny
[semantic transfer](experiments.md#int-11-semantic-runtime-policy) controls do not
establish useful compositional generalization.

**Pending:** [capacity](experiments.md#model-capacity) has committed artifact
identities for small 26k/63k/100k and large 15.6k, not a completed three-seed capacity
verdict. Cancellation and approximately 4% large-model retention are task-reported,
not a committed final analysis here. No intermediate-size **sustained strength
cohort** is evidenced. Smaller/depth variants and a width128 one-update fixture do
exist; “no other size has ever trained” would be false without that qualification.

**Would settle the next decision:** a justified ladder including an intermediate
and/or cheaper model, with paired seeds, fixed input/learning contracts, common
transitions and time, inference costs and retained-sample counts. Keep history,
aggregation and capacity contrasts separate before attributing their interaction.
No model choice is made in this map.

### 4. What experience would teach the missing Lessons-side play?

`learning-experience@1` · **Data**

**Why now:** Jack Heart reports roughly .88 Allies/.41 Lessons against greedy and
judges greedy Allies beatable because of bad attacks. That is a useful behavioral
hypothesis, not evidence of a deck ceiling or a demonstrated blocking defect.
Those values must not be mixed with MTG-118's earlier monitoring splits.

**Known:** [exp-11](experiments.md#exp-11-curriculum-exploitability) found self-play
promising versus random/frozen-student training (two seeds), but in an older world.
[Deck balance](experiments.md#etu-87-allies-lessons-balance) shows lists and pilots
matter; it does not fix an achievable ceiling against current greedy Allies.
[Exp-09](experiments.md#exp-09-control-competency) supplies a reason to inspect
actual delayed plans rather than rename every failure “strategy fusion.”
[Search/distillation](experiments.md#exp-03-distillation) once paid, but
[exp-07](experiments.md#exp-07-expert-iteration), [INT-7](experiments.md#int-7-value-target-comparison)
and [INT-8](experiments.md#int-8-student-signal-guidance) retain negative results.
A calibrated value or plausible belief is not automatically a better player.

**Pending:** [mirror curriculum](experiments.md#mirror-curriculum) has a negative,
tiny pilot and an unfinished two-seed 10k comparison; it changes matchup exposure,
not archived-opponent diversity. Current-self versus an archive/league, a
selected-world combat intervention, and learned-belief/search gains remain untested.

**Would settle the next decision:** finish interpretation of already authorized
mirror and head-to-head evidence, then locate Lessons losses in retained games
(attacks, blocks, removal, resource use). Pair a concrete intervention with
unchanged controls. A population comparison should hold deck exposure fixed; a
combat test needs defensible lines in the actual selected world. Search or belief
work must improve complete play at declared compute, not only label quality.

### 5. Which machine and execution path make each experiment practical?

`machine-fit@1` · **Compute**

**Why now:** missing results have come from storage, setup, transport and time
limits as well as learning. Hardware selection should minimize the cost of a
complete interpretable result, including evaluation and publication.

**Known:** [CPU host probes](experiments.md#distributed-rl) completed once per
host but were confounded by runtime/load. [Laptop scale](experiments.md#laptop-scale)
proved model fit/execution, not RL throughput. [L4/A40 sweeps](experiments.md#model-capacity)
favored L4 on short matched loops; both retained a large batch1024 OOM and setup/
transfer failures. [Detached execution](experiments.md#remote-execution) completed
bounded CUDA work after client exit, exported playable bytes and deleted rentals.
This is meaningful lifecycle evidence, not a universal recovery guarantee.

**Pending:** final capacity cost settlement/cancellation receipts, baseline
sustained timing at a published final revision, and restart disk-failure accounting.
No distributed learning speedup or uncontrolled Mac-versus-GPU strength ranking is
established.

**Would settle the next decision:** phase timings, peak storage/memory and total
cost for the exact recipe, collection geometry and evaluation cohort on each
candidate host; include failures, transfer, checkpoint growth and cleanup reserves.
Use small local controls for feasibility, not as evidence that a full cohort fits.

## Decisions for Jack Heart

1. Is this five-question ranking right, especially evaluation before diagnosing
   the plateau? It is an agent proposal, not a priority change.
2. What opponent/competency result should count as the next convincing strength
   gain? Greedy progress, head-to-head ordering and human-challenger success are
   different acceptance bars.
3. After pending results are committed, is the next contrast late floor/schedule,
   a capacity ladder, or training experience? This document allocates none of them.
4. Does the Lessons weakness warrant a specific combat/blocking diagnostic now?
   The behavioral judgment is Jack Heart's; no causal attribution is made here.
5. Review the [draft findings](findings.md) individually. Reviewing the map must
   not be treated as approving a launch, a recipe change or a chapter claim.

## Provenance and upkeep

- Evidence snapshot: Fantasia `43c6e479c25399665b56b43e2bb6906b1ea37113`.
  Every local source link in the register means **that revision**, not moving main.
  [sources.json](sources.json) records path, exact revision and SHA-256, including
  older compact data references. A report's citation revision is distinct from
  its frozen execution source, world and checkpoint identities.
- Local-only branch evidence is explicitly **pending**, even if committed locally.
  Task-reported live statuses are dated 2026-10-09, not independently polled here.
  Missing final evidence is not evidence that a running experiment failed.
- Coverage: all top-level `experiments/*.md` reports at the snapshot, recent
  evidence documents and software-proof bundles, plus named external/pending work.
  The register retains every report from the prior map. It is not a claim to have
  inventoried every ignored `.runs` directory or every historical test execution.
- Built from the unmerged ideaspace map at
  `52cb5a225ef68a78787d86370d75e0be1c9fd2cb` and Etude's read-only
  `research/manabot` definitions. The former's unchanged summaries are reused as
  drafts; the technique, capacity and history dispositions are reconciled with
  newer evidence. Neither prior map supplies review approval.
- Same conceptual shape as Etude: stable areas, versioned questions, experiment
  source keys and explicit relevance reasons, findings with evidence and limits.
  This Markdown snapshot is **not an importer payload**. Existing Etude question
  IDs are preserved where wording/scope agree; new questions have new IDs.
  A future import must retain its locked definitions, append revisions rather
  than overwrite them, and register evidence before findings. No second research
  runtime or website is introduced.
- Read-only sanity check: `uv run python scripts/check_research_map.py` checks
  report coverage, available pinned source hashes, question attachments and local links.
  Missing local-only branch commits are reported as pending, not validation failures.
  It does not reproduce experiments, verify private bundles or approve findings.

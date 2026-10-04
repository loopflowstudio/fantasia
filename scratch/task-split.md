# Training deliverables after Jack Heart's approved split

2026-10-04: Jack Heart approved three separate Tasks. Preserve all current implementation and keep one writer while the shared contracts settle.

- [ETU-89](https://linear.app/loopflow/issue/ETU-89): executable TrainingRegime/TrainingRun infrastructure, stage contracts, runnable existing-trainer adapters, artifact/cost/budget/failure records.
- [ETU-90](https://linear.app/loopflow/issue/ETU-90/make-direct-self-play-rl-correct-and-test-ataraxos-training-techniques): direct-RL rollout correctness, terminal/boundary advantage and return calculations, independent horizon/estimator/filtering/KL/regularization/schedule/EMA treatments and their focused proofs. Uses ETU-89 contracts and ETU-75 checkpoint admission.
- [ETU-91](https://linear.app/loopflow/issue/ETU-91/compare-learning-speed-and-ataraxos-ablations-with-reproducible): learning-speed comparison and Ataraxos ablation studies, EvaluationProtocol, existing arena/replay, executed notebooks/reports, and concrete follow-up protocols. Depends on ETU-89 and ETU-90.

The original integrated design remains the technical source; these Tasks divide acceptance ownership, not authorization to discard already-written code. Keep separate evidence per Task and map the resulting PR(s) to each Task actually covered. One shared PR is acceptable if its scope and acceptance evidence explicitly cover all three; never claim a Task complete from another Task's smoke alone. No competing worker is being launched. Existing autonomous implementation/publication/landing authorization continues. No paid compute or week-long training run is authorized.

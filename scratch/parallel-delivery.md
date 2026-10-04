# Parallel delivery constraint

ETU-89 is implementing training regimes in parallel from main 3f297533, whose world is w4. Its owner must reuse ordinary checkpoint/loader contracts. This restored ETU-75 checkout starts from older 8448dde9 and its kickoff says w3: sync and realign against current main before finalizing schema/world decisions; do not regress current world to w3. Preserve existing work. Coordinate through the existing owners, not duplicate training abstractions.

# Assumptions

- MTG-131 keeps the existing 25 scheduled pairings, not a new 45-pair full roster
  round robin. “All combinations” means both same-deck matchups and both seats
  within every existing pairing, matching the request to redo the head-to-heads.
- Mirrors need native explicit compiled-pack selection as well as Python admission;
  silently using the generic card registry would change the world. Resolved by
  importing only that prerequisite from 9649f42f, not its training experiment.

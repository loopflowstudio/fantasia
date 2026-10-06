# Release visual references v6

ETU-77 adds Find an action and an unfiltered count above lists of eight or more
legal offers. In the release matrix this intentionally changes only
`prompt-discard.png`: the eight-card cleanup panel grows from 235 × 430 to
235 × 520. Every original label and duplicate remains in order. No rules,
Command, trajectory, asset, or comparison tolerance changes are intended.

The failure at published head `fadffb46f2afb4b1a9d256d6e16c3c81d681208d`
([Linux run 37412543910](https://github.com/loopflowstudio/etude/actions/runs/37412543910))
reported 30,759 changed pixels because v5 lacked these controls. Inspection of
its expected, actual and diff images confirmed the added controls and unchanged
eight choices. The prior macOS check ignored screenshots, so it could not catch
this missing reference-version update.

The v5 PNGs and matrix remain frozen. Generate v6 using the CI
`update_visual_references` workflow, inspect all changed captures, and require
strict comparison before publication. A screenshot-ignored local run proves
behavior only; it cannot certify Linux references or human play acceptance.

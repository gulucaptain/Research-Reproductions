# Articulation in Prime — reviewed local progress snapshot

Paper: [Articulation in Prime: Primitive-Based Articulated Object Understanding from a Single Casual Video](https://arxiv.org/abs/2605.18645). Reviewed 2026-11-16.

**Implementation not published.** This collection stores a permitted generated preview and numerical snapshot; it does not publish the local paper implementation, procedural inputs, learned parameters or raw traces. The public snapshot therefore cannot independently replay the optimization. Local implementation commit: `4c0a9ecdefdf09f234dc6d1a12ba085591d29b21`.

Five mathematical/gradient/visibility tests passed, selected-parameter replay checks passed, and the CPU/MPS full-objective gradient check passed. Paper-shaped CPU/MPS resource checks each completed only 5 iterations on synthetic inputs; they do not establish convergence.

## Initial local results

Independent partial implementation. **No original-paper table is reproduced by these experiments.**
Procedural SQ geometry, 8 frames × 256 visible points; exact camera/depth/kinematic flow.
Q=6, P=4, 128 surface samples, 128×128 visibility raster. These scenes favor the model geometry family.

Completed optimization runs: **30**, excluding smoke/device checks. All seeds remain in `results/summary.json`.

| Suite / case / variant | Seeds | Selected | mIoU | Type acc. | Axis ° | Pivot cm | State ° / cm | State coverage | Missing-part runs |
|---|---|---|---|---|---|---|---|---|---|
| ablations / hinge / no_flow | 0,1,2 | 1 | 0.9523 | 1.0000 | 7.0493 | 134.5157 | 26.6947 / missing | 1.0000 | 2 / 3 |
| ablations / hinge / no_motion | 0,1,2 | 1 | 0.9970 | 1.0000 | 0.0000 | 0.0279 | 0.0470 / missing | 1.0000 | 1 / 3 |
| ablations / hinge / no_visibility | 0,1,2 | 2 | 0.2974 | 0.0000 | missing | missing | missing / missing | 0.0000 | 3 / 3 |
| convergence / hinge / full | 2 | 2 | 0.9879 | 1.0000 | 0.0000 | 23.7281 | 13.7438 / missing | 1.0000 | 0 / 1 |
| pilot / drawer / full | 0,1,2,3,4 | 3 | 0.4607 | 0.0000 | missing | missing | missing / missing | 0.0000 | 5 / 5 |
| pilot / dual / full | 0,1,2,3,4 | 2 | 0.9673 | 0.5000 | 45.0124 | missing | missing / 1.1336 | 0.5000 | 4 / 5 |
| pilot / hinge / full | 0,1,2,3,4 | 2 | 1.0000 | 1.0000 | 0.0280 | 28.0343 | 15.0897 / missing | 1.0000 | 2 / 5 |
| pilot / occluded_hinge / full | 0,1,2,3,4 | 2 | 0.8119 | 0.0000 | 89.9262 | missing | missing / missing | 0.0000 | 4 / 5 |

## Interpretation and limits

- Seed selection uses the final objective within one variant only. Losses from different ablations are not compared for selection.
- Type accuracy is over ground-truth moving joints; missing joints count as incorrect. Missing metrics are not filled with zero.
- Axis/pivot/state means may cover fewer joints than type accuracy. Per-joint details and state coverage are preserved.
- Label matching uses Hungarian IoU. These metrics use the unpruned argmax of the soft hierarchy; author pruning thresholds are unknown.
- The convergence diagnostic re-runs the minimum-loss hinge pilot seed for 10k steps; it is not a new best-of-five 10k result.
- No ViPE/SAM2/GMSF preprocessing, original datasets, or published competing baselines have been run here.
- MPS parity covers one full objective/gradient evaluation, not an entire GPU optimizer trajectory.
- The motion-regularizer ablation sharply improves the local hinge pivot/amplitude result; it is an altered objective, not the paper method result.
- An oracle flow+motion-only diagnostic (using GT labels/joints solely for analysis) favors motion factor 0.665 at the current geometry scale, and 1.0 at 2× scale. This establishes scale sensitivity of that isolated objective, not a complete explanation of all fitting errors.
- An independent sphere-depth oracle finds noticeable coarse-mesh visibility error; inspect `results/visibility_check.json`. This check does not establish Nvdiffrast equivalence.

## Artifacts

- `results/summary.json`: all runs and minimum-loss selections.
- `results/initial_comparison.png`: all pilot seeds and one selected local scene.
- Every run: exact config, input SHA-256, raw trace, learned parameters, prediction and final metrics.
- `results/device_check.json`: CPU/MPS objective and gradient check.
- `COVERAGE.md`: original paper tables and remaining gaps.

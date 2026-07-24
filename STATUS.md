# Open items

Short-lived state that doesn't belong in `data.json`. Keep this pruned — if something here is stale,
delete it. The Sunday review may reference it; nothing reads it automatically.

## Flagged for review — not changed

Found in a consistency audit. Each is a health or judgement decision, so the files were left as they
are. Resolve at the next monthly nutrition review or with a clinician, then delete these entries.

- **Zn:Cu ratio in the magnesium stack is 15:1, not the ~10:1 target.** Both athletes take
  `320 mg Mg + 30 mg Zn + 2 mg Cu + 4.2 mg B6` (`data.json` `nutrition.supplements`), while
  `shared/keto_nutrition_reference.md` sets ~10:1 and `monthly-nutrition-review` audits against it.
  Either the copper is low for that zinc dose, or the 10:1 target is the thing to revise. Note 30 mg
  zinc is also close to the 40 mg UL, and this dose is **shared despite a 35 kg bodyweight
  difference** — the more pressing question is Alicja's 52 kg.
- **Denis's protein now reads 212.8 g/day**, above the 209 g top of the 1.8–2.4 g/kg band the monthly
  review checks (2.45 g/kg at 87 kg). This is a *correction*, not a diet change: the cocoa powder entry
  had `"p": 0` where the shared food table gives 21 g/100 g, so the total was understated by ~3 g and
  had been sitting just inside the band. Decide whether to accept 2.45 g/kg or trim elsewhere.

## Denis

- **FTP test outstanding.** `cycling.ftp` is `null`, so all interval targets are RPE-based until a
  Zwift Ramp Test is done. Do it on a fresh day — not after Monday gym. Report the result to the
  Sunday review, which writes it to `cycling.ftp` and moves any old value to `cycling.history`.
- **No structured block started.** `training_block.md` does not exist; the rolling 3+1 mesocycle is
  covering deloads meanwhile. The Sunday review flags "📦 Block-ready" when the criteria pass —
  run `/start-training-block` then, and activate the `daily-session-brief` scheduled task.
- Mesocycle week 1 began 2026-07-20 after the 2026-07-18 log reset.

## Alicja

- **Needs a GitHub token on her own device** to save log entries from `tools/dashboard.html`
  (⚙︎ in the dashboard; a fine-grained PAT with read/write on this repo's contents). Until then her
  entries have to be logged from a device that has one.
- Calorie total in `data.json` is ~1798 kcal against a ~1900 target for a novice-gain surplus — the
  monthly nutrition review keeps flagging the gap.

## Either athlete pauses training

Tell the assistant, and pause the affected scheduled tasks. The weekly review's gap/return rule
handles resumption on its own (~10–20% load reduction after 2+ weeks off).

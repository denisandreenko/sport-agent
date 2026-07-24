# Open items

Short-lived state that doesn't belong in `data.json`. Keep this pruned — if something here is stale,
delete it. The Sunday review may reference it; nothing reads it automatically.

_Last updated: 2026-07-24_

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

# Alicja — Gym Training Plan (Novice Strength / Hypertrophy)

**The sessions themselves — exercises, set × rep targets, warm-up, working loads (`stub`) — live in
`data.json` `sessions.GYM_A/GYM_B`.** This file holds the *reasoning* and the **bodyweight progression
ladders**, which exist nowhere else. Never restate a load here.

Two full-body sessions on a fixed schedule, **Monday (A)** and **Thursday (B)**, three days apart for
recovery. The goal is a strength and muscle base with clean technique, so the governing rule is
**2–3 reps in reserve on every set — never to failure**, and technique before load. Increase load in
small jumps (1–2 kg on dumbbells).

## Bodyweight progression ladders

Advance a stage only on hitting the **top of the rep range with clean form and 2+ reps in reserve**.
Her current stage is whichever variation `data.json` names as the exercise — don't track it here too.

### Push-up

| Stage | Target |
|---|---|
| Wall push-up | 3 × 12 |
| Incline push-up (hands on bench) | 3 × 10 |
| Knee push-up | 3 × 10 |
| Full push-ups + negatives to fill (slow lower) | 3 × 5 total; advance when all 5 are full |
| Full push-up | 3 × 10 |
| Feet-elevated push-up (feet on a bench) | 3 × 10 |

Once full push-ups reach 6+ reps a set, they are hard enough to build muscle on their own, so no
knee push-up back-off is needed after them.

### Pull-up

| Stage | Target |
|---|---|
| Inverted row (bar at waist, feet down) | 3 × 10 |
| Band/machine assisted pull-up | 3 × 8, reducing assistance over time |
| Negative pull-up (slow lower from top) | 3 × 5 at a 6 s lower |
| Full pull-up | 1 → 3+ |

The assisted and negative stages run **together**: assisted reps build volume through the full
range, negatives build strength at full bodyweight — including the dead-hang bottom, where bands
help most. That also makes pull-ups a twice-a-week movement. Assisted reps alone stalled for 7
weeks (mid-Sep to late Oct 2026) on the same bands. For a negative, she **steps up** from a bench or
box to the top position — never a jump, which arrives with momentum and jerks the shoulders and elbows.

### Core

No named stages — progress hanging side knee raises, tuck reverse crunches and planks by adding reps
or time first, then move to harder variations: hollow hold → straight-leg / hanging leg raises. Judge
the current point from the log rather than from an exercise name.

## Progression & deload

- **Double progression:** add reps within the range on all sets, then add a little load — or move to a
  harder ladder stage for the bodyweight movements.
- **Deload:** cadence is the `mesocycle` object in `data.json` (5+1 — every 6th completed week), or
  earlier when run-down. Cut a set per exercise at the same loads, keep technique, and keep mobility in
  full. No progression into a deload week.
- If a movement causes **joint** pain rather than muscle effort, regress a stage and check form.
- She is a novice by deliberate choice of programming: simple linear progression, no wave loading.

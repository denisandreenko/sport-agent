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
| Negative full push-up (slow lower) | 3 × 5 |
| Full push-up | 3 × 8 |

### Pull-up

| Stage | Target |
|---|---|
| Inverted row (bar at waist, feet down) | 3 × 10 |
| Band/machine assisted pull-up | 3 × 8, reducing assistance over time |
| Negative pull-up (slow lower from top) | 3 × 5 |
| Full pull-up | 1 → 3+ |

### Core

No named stages — progress sit-ups and planks by adding reps or time first, then move to harder
variations in this order: dead bug → hollow hold → leg raises. Judge the current point from the log
rather than from an exercise name.

## Progression & deload

- **Double progression:** add reps within the range on all sets, then add a little load — or move to a
  harder ladder stage for the bodyweight movements.
- **Deload:** cadence is the `mesocycle` object in `data.json` (5+1 — every 6th completed week), or
  earlier when run-down. Cut a set per exercise at the same loads, keep technique, and keep mobility in
  full. No progression into a deload week.
- If a movement causes **joint** pain rather than muscle effort, regress a stage and check form.
- She is a novice by deliberate choice of programming: simple linear progression, no wave loading.

# Workout Log

<!-- FORMAT SPEC (the recommendation engine parses this)
Each entry uses the block below. Keep one blank line between entries. Omit unknown fields.

SESSION_TYPE: any ID from data.json logSessionTypes
Subjective readiness (morning, 1–5 each; 5 = best — for soreness 5 = no soreness):
  sleep, soreness, energy, motivation
RPE: 1–10 (session overall)

READINESS RULE: a rating ≤ 2 is "poor".
  0 poor → GREEN: train as planned
  1 poor → AMBER: keep the session, cut top-end volume ~20%, hold loads
  2+ poor (or clearly bad night) → RED: easy/recovery only; apply removal hierarchy from shared/training_principles.md
-->

<!-- ENTRY TEMPLATE — copy and fill in on phone (or use the dashboard):

## YYYY-MM-DD | SESSION_TYPE
- sleep: X/5
- soreness: X/5
- energy: X/5
- motivation: X/5
- rpe: X/10
- notes: [free text — what felt hard, what moved well, any pain/discomfort]

### Key lifts (GYM sessions only)
Reps = actual reps per set, separated by "/" (e.g. 8/7/6 = set1 8, set2 7, set3 6).
| Exercise | Reps | Load (kg) | Notes |
|---|---|---|---|
| Hack squat | 8/7/6 | 80 | smooth |

### Endurance (cycling/run sessions only)
- duration: Xmin
- avg_power_or_pace: [watts or min/km]
- intervals_completed: X/X
- terrain: [road/gravel/trainer]

-->

<!-- LOG RESET 2026-07-18: all prior entries (2026-05-16 … 2026-06-29, incl. Strava-synced ones) removed for a clean start with the rolling mesocycle (week 1 begins 2026-07-20). History is preserved in git if ever needed. Gym starting loads live in data.json `stub` values. Legacy Garmin fields (hrv_status, body_battery, sleep_score) are gone with the old entries — the parser no longer needs to know about them. -->

---

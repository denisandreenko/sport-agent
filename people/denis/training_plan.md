# Denis — Training Plan

General methodology (readiness, deload, session-type definitions, removal hierarchy, mobility) lives in `shared/training_principles.md`. This file holds Denis's specific weekly structure and priorities.

## Priorities

1. Gravel cycling performance
2. Strength and hypertrophy
3. Calisthenics skills
4. Mobility
5. Optional running/swimming for recovery or maintenance

## Weekly structure template

| Day | Priority |
|---|---|
| Monday | Gym A + short calisthenics push/handstand skill |
| Tuesday | Cycling VO2max / hill repeats |
| Wednesday | Gym B + calisthenics pull skill |
| Thursday | Cycling threshold / sweet spot / tempo |
| Friday | Gym C + short support/core skill |
| Saturday | Long gravel ride |
| Sunday | Recovery, mobility, easy spin/swim/walk, optional easy run |

Cycling session-type definitions and examples are in `shared/training_principles.md`. Gym split detail is in `gym_training_plan.md`; calisthenics focus is in `calisthenics_status.md`.

### Fatigue-stacking guardrails

Cycling is priority #1, so gym legs must not blunt the two key conflict points:

- **Mon (squat) → Tue (VO2max):** keep Monday lower-body at RPE ≤ 8, no leg accessories to failure. If Tuesday's interval power is down, Monday squats went too hard.
- **Fri (hinge + single-leg) → Sat (long ride):** the biggest conflict. Keep Friday's trap-bar deadlift submaximal in volume (quality singles/doubles within the rep range, not grinders) and don't chase leg-accessory burn. If legs are still heavy Saturday, cut deadlift volume — **not** the long ride.
- Don't combine a hard leg gym day, a hard cycling day, and the long ride within ~48 h without an easy day between.

## Running & swimming (optional support)

- **Running:** 0–1 easy run/week, 20–45 min Z1–Z2. No regular running VO2max/threshold or weekly long run unless specifically maintaining running.
- **Swimming:** 0–2 easy swims/week, 20–40 min technique/recovery. Avoid hard swims without a specific reason.

## Cycling block notes

- Long gravel ride: 3–5 h mostly Z1–Z2; occasional tempo finish, climb blocks, rough terrain, fueling practice, handling drills.
- Reduce leg-accessory volume during hard cycling blocks.
- No races/events currently — training for general performance.

## Periodization (micro / meso / macro)

State lives in `data.json` → `mesocycle`; the Sunday weekly review maintains it.

- **Microcycle** = the 7-day template above. Unchanged — it already handles daily fatigue via readiness (🟢🟡🔴) and the stacking guardrails.
- **Mesocycle** = rolling **3+1**: three loading weeks, then a deload week. The review counts *completed* weeks (≥3 logged sessions) — skipped weeks freeze the counter, so deload arrives after 3 weeks of actual accumulated work, not calendar time. Deload week: gym volume −30–40% (per `training_principles.md`), cycling drops one rung below current level as a maintenance dose, long ride ~2 h Z1–Z2 only. Fatigue markers can pull the deload earlier; nothing postpones it.
- **Macrocycle** = the cycling base/build rotation (`cycling.phase`, 4–8 weeks each — i.e. 1–2 mesocycles per phase). Gym runs the same 3+1 wave year-round; what changes across the macro is *which* cycling quality session progresses. No races planned, so no taper/peak structure — if an event appears, add a specialty block toward it.
- **Interaction with `start-training-block`:** an active block suspends the rolling counter — the block brings its own 4-week structure (baseline → accumulation → intensification → deload). The rolling mesocycle is the default state *between* blocks, so deloads now happen with or without a block.

## Cycling progression & FTP (TrainerRoad-style)

Cycling now progresses like the gym lifts — structured, from logged data. State lives in `data.json` → `cycling`.

- **FTP anchor:** Zwift Ramp Test every 6–8 weeks (min 28 days apart, fresh day — not after Mon gym). Result + date go to `cycling.ftp`, previous values to `history`. All interval targets are %FTP; until first test, ride by RPE with HR as sanity check.
- **Progression levels:** each quality session (Tue VO2max, Thu threshold) has an ordered ladder in its session definition. Current rung = `cycling.levels`. Weekly review moves it: all intervals completed at target power/RPE ≤ 8 → +1; partial → hold; failed or 2+ week cycling gap → −1. Never jump rungs.
- **Phases (base/build):** `cycling.phase` rotates emphasis every 4–8 weeks. Base: Thu sweet-spot/threshold ladder progresses, Tue held as maintenance. Build: Tue VO2max progresses, Thu holds. Only ONE quality session progresses at a time — the other is a maintenance dose. Long ride stays Z1–Z2 in both.
- **Retest triggers (between scheduled tests):** interval power up at same RPE/HR two weeks running, or threshold rung feels ≤ RPE 6 — weekly review flags a retest instead of silently inflating levels.
- **Outdoor rides:** no power meter — Saturday is judged by HR/feel only; never by power.

## Do not do by default

- Don't add endurance volume just because capacity exists.
- Don't keep triathlon running intensity unless specifically requested.
- Don't make every ride hard.
- Don't turn calisthenics skill practice into failure training.
- Don't combine hard leg gym, VO2max cycling, and the long ride too close together without recovery.
- Don't recommend strict keto during race simulation if performance fueling is the priority.

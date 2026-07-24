# Gym Training Plan (Strength / Hypertrophy)

**The sessions themselves — exercises, set × rep targets, rest, working loads (`stub`), activation and
mobility lines — live in `data.json` `sessions.GYM_A/GYM_B/GYM_C`.** This file holds only the
*reasoning*: why the split looks like this, why particular things were added or removed, and how
progression works. Never restate a load here; the Sunday review updates `data.json` and any copy in
this file would silently go stale.

## The split

Mon **Day A** (squat / horizontal push / vertical pull) · Wed **Day B** (pull / overhead press / arms /
core) · Fri **Day C** (hinge / incline push / single-leg). Roughly **59 working sets/week** across three
50–55 min sessions including activation and mobility.

- **Squat and hinge patterns sit on different days** to limit cumulative lumbar stress.
- **Heavy leg days (Mon squat, Fri hinge) sit either side of the cycling week** — the two conflict
  points are Mon→Tue VO2max and Fri→Sat long ride. The guardrails are in `training_plan.md`; the
  practical consequences are:
  - Monday's hack squat stays at RPE ≤ 8 because Tuesday is VO2max. If Tuesday's interval power is
    down, Monday went too hard. Machine load is not comparable to barbell squat.
  - Friday's trap bar deadlift is **quality reps, not grinders**, and drops a set on amber/red
    readiness. If legs are heavy Saturday, cut deadlift volume — never the long ride.
- **Day B carries no heavy axial loading** by design, so the mid-week gym day doesn't compound the
  Monday/Friday spinal load.
- **Core is covered by pattern, not volume:** anti-rotation (Pallof, Day A), anti-extension (ab wheel,
  Day B), flexion (cable crunch, Day C).
- Seated DB overhead press is kept partly as the **strength base for handstand work**.
- **No supersets** in the written plan — full rest between exercises as prescribed.
- **Friday evening is rest** — no PM endurance after Day C, to protect Saturday's long ride.

## Deliberate omissions and changes

- **Day A standing calf raise removed (2 sets):** soleus is trained Friday via seated calf raise and
  calves get heavy work cycling, so marginal value was low — and trimming Monday leg volume protects
  Tuesday's VO2max session. Re-add only if calf hypertrophy becomes a specific goal.
- **Bench press re-entry:** the working load was set ~10% below a prior *grinding* flat bench rather
  than matched to it. Current value is the `stub` in `data.json`.

## Post-recovery reintroductions (when pain-free)

No active injuries, so these are available. Add **one at a time** and only if symptom-free:

- **Plyometrics** (after activation, before the first main lift) — pick one of band-resisted pogos, box
  jumps, medicine ball slam, plyo push-ups. 2–3 × 3–5 reps, ~3–4 min. Prefer Day A and/or Day C.
- **Bilateral barbell hip thrust** on Day A (3 × 10–12, from roughly 80 kg) replacing the single-leg
  hip thrust once the glute pattern is stable.
- **Back squat** — only if symptom-free; start around 85–90 kg, or alternate weeks with hack squat.
  Stop immediately if sacral/coccyx symptoms return.
- **Handstand skill** (outside the gym) — wall holds, wall walks, pike push-up progressions, 10–15 min
  2–3×/week on non-gym days or after mobility.

## Progression

- **Compounds** (hack squat, bench, trap bar deadlift, weighted pull-ups): hit the prescribed RPE each
  session; add load when all sets reach the **top of the rep range** at that RPE.
- **Accessories:** double progression — add reps within the range on all sets first, then increase load.
- **Deload:** cadence and magnitude are the `mesocycle` object in `data.json` (3+1) and
  `shared/training_principles.md`. No load progression into a deload week.
- Single-leg hip thrust starts at bodyweight and adds a bar once the pattern holds under load — judge
  that from the log, not from a week number.

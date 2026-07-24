# Denis — Calisthenics Status

Current skill levels and focus. Ladder definitions are in `shared/calisthenics_ladders.md`.
Skill work stays **frequent, low-fatigue, and technical** (3×/week, 10–15 min) — never to failure. Advance a level only when the **target** is met with clean form.

<!-- SKILL_STATE — machine-readable current level (dashboard + assistant read this; update on level-up)
muscle_up: 4/5
one_arm_pull_up: 1/6
front_lever: 2/6
back_lever: 2/5
hefesto: 1/6
planche: 2/6
handstand_push_up: 3/5
one_arm_push_up: 3/8
one_arm_handstand: 4/11
v_sit: 3/8
dragon_flag: 5/7
human_flag: 2/8
pistol_squat: 8/8
shrimp_squat: 4/5
last_reviewed: 2026-06-14
-->

Levels are in the SKILL_STATE block above and nowhere else — it used to be mirrored in a snapshot
table here, which meant every level-up had to be written twice. Stage names for each level come from
`shared/calisthenics_ladders.md`.

## Recommended focus (track all 14, actively train ~5)

Several skills are near completion — push those rather than spreading thin. Avoid stacking three straight-arm holds (planche + front lever + back lever): build **Front Lever** now, park the other two. Pistol Squat is done → maintenance only.

**Primary (train now — all near a milestone):**
1. **Muscle Up** — one rung from strict; clean the kip → strict
2. **Handstand line:** One Arm Handstand + Handstand Push Up — freestanding handstand, then full wall HSPU
3. **Front Lever** — chosen straight-arm pull; adv. tuck → one leg
4. **Dragon Flag** — one rung from full; strong core carryover
5. **Shrimp Squat** — finish the single-leg set now that pistol is mastered

**Secondary (light touch when fresh):** V-Sit.
**Parked (tracked only):** Planche, Back Lever, One Arm Pull Up, One Arm Push Up, Human Flag, Hefesto. Promote one when a primary graduates.
**Mastered (maintenance):** Pistol Squat — a few quality reps/leg in warm-ups; don't chase it.

Weekly allocation by gym day (skills **before** fatigue, technical, never to failure):

| Day | Focus | Primary drills |
|---|---|---|
| Mon (Gym A) | Push / handstand | One Arm Handstand (adv. wall → freestanding) + Wall HSPU |
| Wed (Gym B) | Pull | Muscle Up (kip → strict transition) + Front Lever (adv. tuck → one leg) |
| Fri (Gym C) | Core | Dragon Flag (one leg → straddle) + V-Sit (tuck L-sit → straddle) |

*Shrimp Squat:* a few low-volume sets in the Monday warm-up (keep leg fatigue minimal — Tuesday is VO2max, Saturday is the long ride).

## How this updates

- The `SKILL_STATE` comment block above is the single source of truth for current levels — the dashboard reads it and the assistant edits it on level-up.
- Advance a level only when the **target** in `shared/calisthenics_ladders.md` is met with clean form, not by calendar.
- Reassess at the **Sunday weekly review**, which is what checks exit criteria and advances levels — the
  monthly review is nutrition-only. Note progress in `workout_log.md` under `CALISTHENICS` entries.

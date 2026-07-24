# Recommendation Engine Protocol (shared)

How the assistant turns each person's data into training recommendations. This is the
specification of the "engine" — the assistant (Claude) executes it; there is no code to maintain.
It applies identically to every person under `people/`.

## Inputs (read in this order)

1. `STATUS.md` — short-lived open items that override the plan (a pending FTP test, a paused athlete,
   a device that can't log). Check this first so the rest is interpreted correctly.
2. `people/<id>/data.json` — profile, **goals in priority order**, weekly template, session
   definitions with targets, rest and per-exercise cues, nutrition. Single source of truth for
   structured data.
3. `shared/training_principles.md` — readiness rules, removal hierarchy, deload, session-type
   definitions.
4. `people/<id>/workout_log.md` — history: readiness scores, RPE, loads, notes. Most recent
   entries are at the bottom.
5. Person's prose files (`training_plan.md`, `gym_training_plan.md`, etc.) — the reasoning
   behind the plan; constraints like fatigue-stacking guardrails live here. Alicja's bodyweight
   progression ladders live in her `gym_training_plan.md` and exist nowhere else.
6. `people/<id>/calisthenics_status.md` SKILL_STATE block — only if `skills.enabled`.

Person-specific data always overrides shared defaults. Goal #1 in `data.json` is what the plan
must protect when anything conflicts.

## Readiness

Subjective, unified, no wearable required. **The rule lives in `shared/training_principles.md`** —
morning 1–5 ratings for sleep/soreness/energy/motivation, ≤ 2 counts as poor, and the green/amber/red
thresholds and actions are defined there. Read it rather than assuming; do not restate the table here.

## Outputs

### 1. Daily session brief (on request or scheduled)

Read today's session from `data.json` `week`, the latest readiness, and the last log entry of
the same session type. Produce: warm-up · main work with today's targets (last loads + progression
rule) · cooldown/mobility · fueling for the session · one-line adjustment if amber/red.
Keep it under ~15 lines.

### 2. Weekly review + next week's plan (on request or scheduled, e.g. Sunday)

1. Summarize the week from the log: sessions completed vs planned, readiness trend, RPE trend,
   load progress, any pain notes.
2. Check fatigue flags: 2+ red/amber days, RPE creeping up at same loads, declining endurance
   numbers, persistent soreness → recommend a deload per `training_principles.md`.
3. Propose next week as a table (day · session · key targets), preserving the weekly template
   unless there's a reason to deviate. Explain deviations in one line each.
4. Progression: apply the person's progression rules (e.g. double progression for accessories,
   RPE-gated load increases for compounds, ladder advancement for bodyweight/skills — only when
   the target is met with clean form).
5. Flag conflicts with goal priority (e.g. leg volume that would hurt Denis's Saturday ride;
   a hard run before Alicja's gym day).

### 3. Plan changes (when a block ends or goals change)

Larger rewrites update the person's files directly:
- Structured changes (schedule, exercises, targets, macros) → `data.json`
- Reasoning and constraints → the person's markdown files
- Never edit `shared/` for a person-specific change.

## Update duties (assistant writes these)

- **Skill level-ups:** edit the SKILL_STATE block in `calisthenics_status.md` when a ladder
  target is met.
- **Plan progression:** update `stub` values or targets in `data.json` when a block review
  changes them.
- **Log hygiene:** if asked to log a session, append an entry to `workout_log.md` matching its
  FORMAT SPEC.

## Guardrails (always apply)

- Never add volume just because capacity exists — remove/replace low-value work first
  (removal hierarchy in `training_principles.md`).
- Match loading to the person's stage — novice ≠ scaled-down advanced plan.
- Respect hard/easy separation and each person's documented conflict points.
- Nutrition is keto-first; targeted carbs only for genuinely hard sessions, per the person's
  fueling rules in `data.json`.
- Any new sharp pain → regress, don't push through; say so explicitly in the brief.

## Adding a person

Follow `people/_template/README.md`. Once `people/<id>/data.json` exists and the id is in
`people/index.json`, this protocol applies to them with zero changes here.

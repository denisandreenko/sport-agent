# Adding a new person

1. Copy this folder to `people/<id>/` (lowercase, no spaces — e.g. `people/marek/`).
2. Fill in `data.json` — it drives the dashboard and the recommendation engine:
   - `profile`, `goals` (priority order matters — the engine plans around goal #1)
   - `week` — weekly template, keyed by day (`0` = Sunday … `6` = Saturday), values are session IDs from `sessions`
   - `sessions` — every session the person does. `kind` is one of:
     - `gym` — renders exercise table with target + last-load tracking
     - `endurance` — renders purpose / interval options / fueling
     - `mobility` — renders exercise/duration list
     - `rest` — renders the note only
   - `dashboard.tabs` — which tabs show: `today`, `log`, `skills` (needs `skills.enabled`), `nutrition`
   - `nutrition` — immutable in the dashboard; edit this file to change it
   - Macro keys in meals: `p` protein, `c` carbs, `f` fat, `fiber`, `kcal` (grams/kcal)
3. Rename `workout_log.md` fields if needed and keep its FORMAT SPEC comment — the engine parses it.
4. Add prose files as needed (`training_plan.md` for the "why" behind the schedule, etc.). Keep data in `data.json`, reasoning in markdown.
5. Add the id to `people/index.json` (this is what the dashboard's person switcher reads).
6. Open the dashboard: `tools/dashboard.html?person=<id>`.
7. Tell the assistant a new person exists so it reads `people/<id>/` — the recommendation
   protocol (`shared/recommendation_protocol.md`) applies to them with no other changes.

Don't edit `people/_template/` itself except to improve the template.

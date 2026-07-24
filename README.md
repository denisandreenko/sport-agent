# Athlete Training

Expandable training + nutrition framework. Currently two athletes (**Denis**, **Alicja**);
adding another is copying a folder — see `people/_template/README.md`.

## Structure

```
athlete-training/
├── README.md                       ← this file
├── CLAUDE.md                       ← standing instructions loaded every session
├── STATUS.md                       ← short-lived open items (FTP test pending, etc.)
├── MIGRATION.md                    ← Cowork → Claude Code migration runbook
├── .claude/
│   ├── settings.json               ← tool permissions (which git commands are pre-approved)
│   └── skills/                     ← the four recurring workflows; each SKILL.md is the live prompt
│       └── README.md               ← how they fit together + restore steps for a new machine
│
├── shared/                         ← methodology & reference (applies to everyone)
│   ├── assistant_instructions.md   ← how the AI assistant works with this repo
│   ├── recommendation_protocol.md  ← the recommendation engine spec (inputs → outputs → guardrails)
│   ├── training_principles.md      ← readiness, deload, session types, removal hierarchy, mobility
│   ├── calisthenics_ladders.md     ← skill-progression ladder definitions
│   └── keto_nutrition_reference.md ← per-100 g food table, TKD fueling, electrolytes
│
├── people/
│   ├── index.json                  ← list of person ids (dashboard person switcher)
│   ├── _template/                  ← copy this folder to add a person
│   ├── denis/
│   │   ├── data.json               ← ALL structured data: profile, goals, week, sessions, nutrition
│   │   ├── profile.md              ← prose background (history, capacity, equipment)
│   │   ├── training_plan.md        ← reasoning: priorities, guardrails, weekly logic
│   │   ├── gym_training_plan.md    ← gym split detail & progression rules
│   │   ├── calisthenics_status.md  ← SKILL_STATE (current levels) + focus
│   │   └── workout_log.md          ← history; logged via dashboard
│   └── alicja/
│       ├── data.json
│       ├── profile.md
│       ├── training_plan.md
│       ├── gym_training_plan.md
│       ├── mobility_splits.md
│       ├── running_plan.md
│       └── workout_log.md          ← manual log
│
├── tools/
│   └── dashboard.html              ← ONE dashboard for everyone: ?person=<id>
```

## Design rules

- **`data.json` = data, markdown = reasoning.** Anything a tool renders (schedule, exercises,
  targets, macros, supplements) lives in `data.json`. The *why* lives in markdown.
- **One dashboard, config-driven.** `tools/dashboard.html?person=denis` — tabs, sessions, and
  colors come from that person's `data.json`. Nutrition tab is read-only by design.
- **Readiness is subjective and identical for everyone:** morning 1–5 ratings for sleep,
  soreness, energy, motivation → green/amber/red (rule in `shared/training_principles.md`).
  No wearable required.
- **The engine is the assistant.** `shared/recommendation_protocol.md` defines how plans,
  daily briefs, and weekly reviews are generated from `data.json` + logs + readiness.

## Dashboard

Open `tools/dashboard.html?person=<id>` (GitHub Pages or locally via any static server).
Reading works without credentials on Pages; **saving log entries needs a GitHub fine-grained
token** (repo contents read/write) entered via ⚙︎ — stored only in that browser.

## Using the assistant

Say **whose** plan you mean. The assistant follows `CLAUDE.md` plus
`shared/assistant_instructions.md`, and generates recommendations per
`shared/recommendation_protocol.md`.

The recurring workflows are project skills, invocable by name in any session:

| Command | What it does |
|---|---|
| `/daily-session-brief` | Today's session for Denis with last loads, readiness, fueling. Read-only. |
| `/weekly-review-and-plan` | Sunday review for both athletes; progresses loads and plans next week. Commits. |
| `/start-training-block` | Builds Denis a 4-week periodized block. Manual, commits. |
| `/monthly-nutrition-review` | Supplement + macro audit for both. Read-only. |

The first, second and fourth also run on a schedule — see `.claude/skills/README.md`.

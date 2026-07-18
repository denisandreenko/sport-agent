# Athlete Training

Expandable training + nutrition framework. Currently two athletes (**Denis**, **Alicja**);
adding another is copying a folder — see `people/_template/README.md`.

## Structure

```
athlete-training/
├── README.md                       ← this file
├── automation/                     ← Claude scheduled-task mirrors + restore guide
│   ├── README.md                   ← how to restore the workflow on a new machine
│   └── tasks/                      ← one file per scheduled task (frontmatter + prompt)
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

Say **whose** plan you mean. The assistant follows `shared/assistant_instructions.md` and
generates recommendations per `shared/recommendation_protocol.md`.

# Automation — Claude Scheduled Tasks & Workflow Restore Guide

This folder makes the training workflow **portable**. The repo's markdown/JSON files hold all training *state*, but the automation lives in Claude (Cowork) scheduled tasks on a specific machine. If this repo is cloned to a new laptop, everything can be restored from here.

## How to restore (tell Claude this on the new machine)

> "Restore the scheduled tasks defined in `automation/tasks/` of this repo."

Claude should then, for each file in `tasks/`:

1. Read the frontmatter (taskId, description, schedule, enabled state) and the prompt body.
2. Replace every occurrence of `{REPO_ROOT}` in the prompt with the absolute path of the local clone.
3. Create the task with `create_scheduled_task` (cron expressions are **local time**).
4. Set the enabled state to match the frontmatter (`enabled: false` → create, then disable).

After restoring, click "Run now" on `weekly-review-and-plan` once to pre-approve its tools (git, file edits) so future runs don't pause on permission prompts.

## The workflow at a glance

| Task | Schedule | Enabled | Role |
|---|---|---|---|
| `daily-session-brief` | 07:45 daily | **no** (enable when a training block starts) | Denis's morning brief: today's session, last loads, readiness call, cycling ladder rung + watts, skill add-on, fueling. Read-only. |
| `weekly-review-and-plan` | Sun 18:00 | yes | The engine. Reviews both athletes, progresses gym loads / calisthenics skills / cycling levels, maintains mesocycle counters and deloads, flags FTP retests and block readiness, plans next week. Only task that commits on a schedule. |
| `start-training-block` | manual | yes | Builds Denis a deliberate 4-week overload block (`training_block.md`). Manual by design — commits 4 weeks of calendar. The Sunday review flags "📦 Block-ready" when criteria pass. |
| `monthly-nutrition-review` | 1st Sun 19:00 | yes | Nutrition + supplement safety audit for both (doses per bodyweight, macros, bloodwork checklist). Read-only. |

## Key design rules (context for any agent operating this repo)

- **State lives in the repo, not in chat**: `people/<id>/data.json` (structured: sessions, ladders, cycling FTP/levels/phase, mesocycle counters, nutrition) + markdown files (plans, logs, skill state). `shared/recommendation_protocol.md` defines how recommendations are produced.
- **Commit scopes are strict**: scheduled tasks may only edit the files named in their prompts, staged by name — never `git add -A`.
- **Mesocycles are rolling**: Denis 3+1, Alicja 5+1, counted in *completed* weeks (≥3 logged sessions); skips freeze the counter; fatigue pulls deloads earlier, never later. An active `training_block.md` suspends Denis's counter.
- **Cycling is TrainerRoad-style**: all intensity as %FTP (`cycling.ftp`, Zwift Ramp Test every 6–8 weeks), ordered interval ladders with per-zone levels, base/build phase rotation. Outdoor rides are HR/feel only (no power meter).
- **Never cram missed sessions**; gap/return rules are in the weekly review prompt.
- **Readiness is subjective** (sleep/soreness/energy/motivation 1–5, logged via `tools/dashboard.html`); no wearable parsing.

## Maintenance rule

The files in `tasks/` are mirrors of the live scheduled-task prompts. **Whenever a live prompt is changed, update the mirror in the same session and commit it.** If mirror and live task ever disagree, the mirror in git is the source of truth.

## Not covered by this folder

- Dashboard saving requires a GitHub token per device (⚙︎ in `tools/dashboard.html`).
- Claude's personal memory (athlete profile summaries) is machine-local convenience only; everything needed is in this repo.

There is **no automatic ride sync** (Strava integration was removed) — all sessions are logged manually via the dashboard. Older log entries marked "Auto-synced from Strava" are historical.

# Recurring workflows

Four prompts drive this repo. Each is a **project skill**: the file here is the live prompt — there is
no separate copy anywhere to keep in sync. Invoke any of them by hand as `/<name>`, or let the
scheduled ones fire.

| Skill | Schedule | State | Commits? | Role |
|---|---|---|---|---|
| `weekly-review-and-plan` | Sunday 18:00 | Active | **yes** | The engine. Reviews both athletes, progresses gym loads / calisthenics skills / cycling levels, maintains mesocycle counters and deloads, flags FTP retests and block readiness, plans next week. |
| `daily-session-brief` | daily 07:45 | **Paused** | no | Denis's morning brief: today's session, last loads, readiness call, cycling ladder rung + watts, skill add-on, fueling. Activate when a training block starts. |
| `start-training-block` | Manual | Active | **yes** | Builds Denis a deliberate 4-week overload block (`people/denis/training_block.md`). Manual by design — it commits four weeks of calendar. The Sunday review flags "📦 Block-ready" when the criteria pass. |
| `monthly-nutrition-review` | 1st Sunday 19:00 | Active | no | Nutrition + supplement safety audit for both (doses per bodyweight, macros, bloodwork checklist). |

The two that commit carry `disable-model-invocation: true`, so ordinary conversation can't trigger
them — only an explicit `/name` or a scheduled run.

## What lives where

| | Path | In git |
|---|---|---|
| The prompts | `.claude/skills/<name>/SKILL.md` | ✅ |
| Tool allow/deny rules | `.claude/settings.json` | ✅ |
| Scheduled-task registration | `~/.claude/scheduled-tasks/<name>/SKILL.md` | ❌ user-level only |
| Schedule, folder, model, enabled state | Desktop Routines UI | ❌ not stored in any file |

Claude Code has no project-scoped location for scheduled tasks, which is why the registration is a
thin stub and the substance lives here.

## Restoring on a new machine

1. Clone the repo and trust the folder in Claude Code Desktop.
2. For each of the four skills, create `~/.claude/scheduled-tasks/<name>/SKILL.md`:

   ```markdown
   ---
   name: weekly-review-and-plan
   description: Sunday weekly review for Denis + Alicja
   ---

   Read `.claude/skills/weekly-review-and-plan/SKILL.md` in this project and follow it exactly.
   ```

   Or just ask Claude in a Desktop session: *"set up a weekly task, Sunday 6pm, in the
   athlete-training folder, that reads `.claude/skills/weekly-review-and-plan/SKILL.md` and follows
   it."*
3. Set schedule, folder, and enabled state per the table above. Routines presets cover Manual, Hourly,
   Daily, Weekdays and Weekly — the monthly review's "first Sunday" has no preset, so set it in plain
   language.
4. Click **Run now** on each task and choose "always allow" for each permission prompt. Approvals
   persist per task; without this, unattended runs stall waiting for you.
5. Enable **Keep computer awake** (Settings → Desktop app → General) if the Sunday review matters.
   Tasks only fire while the app is open and the Mac is awake; a closed lid still sleeps.

Missed runs: Desktop starts one catch-up run for the most recently missed slot within 7 days. Both
time-sensitive prompts carry a late-run guard so a Monday-night catch-up doesn't silently review the
wrong window.

## Key design rules (context for any agent operating this repo)

- **State lives in the repo, not in chat**: `people/<id>/data.json` (structured: sessions, ladders,
  cycling FTP/levels/phase, mesocycle counters, nutrition) + markdown files (plans, logs, skill
  state). `shared/recommendation_protocol.md` defines how recommendations are produced.
- **Commit scopes are strict**: each skill may only edit the files named in its own prompt, staged by
  name — never `git add -A`. `.claude/settings.json` allows only those paths and denies the bulk-add
  forms, but the prompt is still the primary constraint.
- **Mesocycles are rolling**: Denis 3+1, Alicja 5+1, counted in *completed* weeks (≥3 logged
  sessions); skips freeze the counter; fatigue pulls deloads earlier, never later. An active
  `training_block.md` suspends Denis's counter.
- **Cycling is TrainerRoad-style**: all intensity as %FTP (`cycling.ftp`, Zwift Ramp Test every 6–8
  weeks), ordered interval ladders with per-zone levels, base/build phase rotation. Outdoor rides are
  HR/feel only (no power meter).
- **Never cram missed sessions**; gap/return rules are in the weekly review prompt.
- **Readiness is subjective** (sleep/soreness/energy/motivation 1–5, logged via
  `tools/dashboard.html`); no wearable parsing.

## Not covered here

- Dashboard saving requires a GitHub token per device (⚙︎ in `tools/dashboard.html`).
- Claude Code's auto-memory (`~/.claude/projects/<project>/memory/`) is machine-local convenience
  only and is not committable. Everything needed is in this repo; short-lived open items go in
  `STATUS.md`.
- There is **no automatic ride sync** (Strava integration was removed) — all sessions are logged
  manually via the dashboard. Older log entries marked "Auto-synced from Strava" are historical.

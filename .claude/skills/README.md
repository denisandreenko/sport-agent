# Recurring workflows

Four prompts drive this repo. Each is a **project skill**: the file here is the live prompt — there is
no separate copy anywhere to keep in sync. Invoke any of them by hand as `/<name>`, or let the
scheduled ones fire.

| Skill | Schedule | State | Folder | Commits? | Role |
|---|---|---|---|---|---|
| `weekly-review-and-plan` | Sunday 18:00 | Active | repo root | **yes** | The engine. Reviews both athletes, progresses gym loads / calisthenics skills / cycling levels, maintains mesocycle counters and deloads, flags FTP retests and block readiness, plans next week. |
| `daily-session-brief` | daily 07:45 | **Paused** | repo root | no | Denis's morning brief: today's session, last loads, readiness call, cycling ladder rung + watts, skill add-on, fueling. Activate when a training block starts. |
| `start-training-block` | Manual | Active | repo root | **yes** | Builds Denis a deliberate 4-week overload block (`people/denis/training_block.md`). Manual by design — it commits four weeks of calendar. The Sunday review flags "📦 Block-ready" when the criteria pass. |
| `monthly-nutrition-review` | 1st Sunday 19:00 | Active | repo root | no | Nutrition + supplement safety audit for both (doses per bodyweight, macros, bloodwork checklist). |

The two that commit carry `disable-model-invocation: true`, so ordinary conversation can't trigger
them — only an explicit `/name` or a scheduled run. **If a scheduled run of one of those two ever does
nothing at all**, that flag is the first suspect: switch its stub body to the "read the file and follow
it" wording below, which doesn't depend on slash-invocation semantics.

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

**A late start is normal, not a fault.** Each task gets a small deterministic delay to stagger API
traffic, so the 18:00 review actually firing around 18:06 is expected behaviour — the old Cowork tasks
did the same thing.

**Permission-rule syntax gotcha:** the space before `*` is significant. `Bash(git diff *)` matches,
`Bash(git diff*)` does not, and neither form matches a *bare* `git diff` — which is why
`.claude/settings.json` lists both the bare and starred forms of the git commands the prompts
prescribe. Get this wrong and an unattended run stalls waiting for approval.

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

## Alternative runners considered

**launchd + headless CLI** — the fallback if depending on the Desktop app being open turns out to be
the wrong trade. Because the prompt bodies live here rather than in the task registration, switching
requires no prompt changes, only a different runner:

```bash
cd /path/to/athlete-training
claude -p "Read .claude/skills/weekly-review-and-plan/SKILL.md and follow it exactly." \
  --permission-mode acceptEdits \
  --output-format json >> ~/Library/Logs/athlete-training/weekly.jsonl 2>&1
```

Wrap in a plist with `StartCalendarInterval`, which fires on wake if a run was missed — plain cron just
skips. Trade-offs versus Desktop: no interactive review of a task that commits, permissions must be
pre-granted more broadly, and you own logging and failure alerting.

**Cloud routines** — rejected. They run from a fresh clone with no local file access, so commits would
come from the cloud runner and the dashboard's browser->GitHub-API write path is out of reach. The
1-hour minimum interval would have been fine; the file access is not.

**A committed subagent definition** — `start-training-block` spawns a sports-science consultant
subagent inline via its prompt. Promoting that to `.claude/agents/sports-science-consultant.md`, a
reusable definition with its own tools and model, is a reasonable follow-up.

## Not covered here

- Dashboard saving requires a GitHub token per device (⚙︎ in `tools/dashboard.html`).
- Claude Code's auto-memory (`~/.claude/projects/<project>/memory/`) is machine-local convenience
  only and is not committable. Everything needed is in this repo; short-lived open items go in
  `STATUS.md`.
- There is **no automatic ride sync** (Strava integration was removed) — all sessions are logged
  manually via the dashboard. Older log entries marked "Auto-synced from Strava" are historical.

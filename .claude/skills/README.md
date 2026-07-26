# Recurring workflows

Four prompts drive this repo. Each is a **project skill**: the file here is the live prompt — there is
no separate copy anywhere to keep in sync. Invoke any of them by hand as `/<name>`, or let the
scheduled ones fire.

| Skill | Schedule | State | Folder | Commits? | Role |
|---|---|---|---|---|---|
| `weekly-review-and-plan` | Sunday 18:00 | Active | repo root | **yes** | The engine. Reviews both athletes, progresses gym loads / calisthenics skills / cycling levels, maintains mesocycle counters and deloads, flags FTP retests and block readiness, plans next week. |
| `daily-session-brief` | daily 07:45 | **Paused** | repo root | no | Denis's morning brief: today's session, last loads, readiness call, cycling ladder rung + watts, skill add-on, fueling. Activate when a training block starts. |
| `start-training-block` | not registered — run `/start-training-block` | — | repo root | **yes** | Builds Denis a deliberate 4-week overload block (`people/denis/training_block.md`). Manual by design — it commits four weeks of calendar. The Sunday review flags "📦 Block-ready" when the criteria pass. |
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

## Setting up the Desktop routines

Do this once per machine. Three routines, ~10 minutes. The prompts are already in the repo — this only
wires up the scheduling.

### 0. Prerequisites

Claude Code Desktop installed, this repo cloned, and the folder **trusted** in Desktop. Routines can't
be saved against an untrusted folder, and Desktop will prompt you to trust it if you haven't.

### 1. Check the skills load before scheduling anything

Open a session on the repo and type `/`. All four skills should appear. Then run a read-only one as a
smoke test:

```
/daily-session-brief
```

It should produce a brief and change nothing — confirm with `git status`. If the skills don't appear in
the menu, stop: nothing below will work until they do.

### 2. Create the weekly review

Sidebar → **Routines** → **New routine** → **Local**. Fill in:

| Field | Value |
|---|---|
| Name | `weekly-review-and-plan` |
| Description | Sunday weekly review for Denis + Alicja |
| Instructions | ``Read `.claude/skills/weekly-review-and-plan/SKILL.md` in this project and follow it exactly.`` |
| Folder | this repo's root |
| Worktree | off — it needs to commit to the real working copy |
| Schedule | **Weekly** → Sunday → 18:00 |

Keep the instructions to that one line. The point of the split is that the real prompt stays in git; a
second copy in the routine would be the drift problem all over again.

### 3. Create the daily brief, then pause it

Same form:

| Field | Value |
|---|---|
| Name | `daily-session-brief` |
| Instructions | ``Read `.claude/skills/daily-session-brief/SKILL.md` in this project and follow it exactly.`` |
| Folder | this repo's root |
| Schedule | **Daily** → 07:45 |

Save, then open it and set **Status → Paused**. It earns its place once a training block is running or
FTP is tested; until then the weekly template is stable and the brief mostly restates it. Flip it to
Active whenever you want it — it's read-only and commits nothing.

### 4. Create the monthly nutrition review — by asking, not by form

The presets are Manual, Hourly, Daily, Weekdays and Weekly. "First Sunday of the month" isn't among
them, so create this one conversationally in any Desktop session:

> Set up a local scheduled task called `monthly-nutrition-review`, in the athlete-training folder,
> running at 19:00 on the first Sunday of each month, whose instructions are:
> Read `.claude/skills/monthly-nutrition-review/SKILL.md` in this project and follow it exactly.

### 5. Don't register `start-training-block`

It's manual-only and it's already a project skill, so `/start-training-block` in any session does
exactly what a Manual routine's **Run now** would. Registering it just creates another thing to keep in
sync.

### 6. Pre-approve the permissions

This is the step that makes unattended runs work. On `weekly-review-and-plan`, click **Run now** and
choose **"always allow"** at every permission prompt. Approvals persist per task and are revocable from
the task's detail page. Skip this and the first real Sunday run stalls silently, waiting for a click.

Then check what it actually did:

```bash
git log -1 --stat
```

It must have staged **only** `data.json` and/or `calisthenics_status.md`. Anything else means the
commit-scope instructions aren't being followed — investigate before trusting it unattended.

### 7. Copy the git allow rules to the user-level settings

The Desktop docs name `~/.claude/settings.json` specifically as the file whose allow rules apply to
scheduled-task sessions. Whether the project-level `.claude/settings.json` also applies is unverified,
so copy the `permissions.allow` block across as well. If step 6 stalled on a git permission, this is
why.

### 8. Keep the machine awake

Settings → **Desktop app → General** → **Keep computer awake**, if the Sunday review matters. Tasks
only fire while the app is open and the Mac is awake; closing the lid still sleeps it.

### 9. Confirm

Ask in any Desktop session: *"show me my scheduled tasks."* Expect three, with the monthly one's next
run landing on the first Sunday of next month rather than weekly — that's the setting most likely to
have been misread.

### 10. Only then, retire the old Cowork tasks

The Cowork copies are paused, not deleted, so they cost nothing as a fallback. Sit through one real
Sunday review on the new setup before deleting them.

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

**Cloud routines** (`/schedule` in the CLI) — not chosen, but a closer call than it first appeared.
They run on Anthropic infrastructure from a fresh clone, need no machine on, and push to
`claude/`-prefixed branches by default, which would give a PR-per-change workflow for free. The
"no local file access" objection is weak here: all state is committed, and the dashboard talks to the
GitHub API from the browser regardless of where Claude runs. Real trade-offs are the 1-hour minimum
interval, a daily run cap, commits carrying your GitHub identity, and research-preview status. Worth
revisiting if the app-must-be-open constraint becomes annoying.

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

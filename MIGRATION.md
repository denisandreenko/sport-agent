# Migration: Cowork → Claude Code

Moving this project from Claude desktop **Cowork** mode to **Claude Code** (CLI + Desktop app), so that
work happens against git and the filesystem directly.

Target: **Claude Code Desktop scheduled tasks**, with every task prompt living **in the repo** under
`.claude/skills/`.

## Status

Executed on branch `migrate-to-claude-code`, 2026-07-24. Everything that lives inside the repo is
done; what's left needs the Desktop app or a path outside the repo.

**Done (in this commit)**

- [x] `.claude/skills/<name>/SKILL.md` × 4 — moved with `git mv`, so history follows (§4.3)
- [x] Frontmatter rewritten to `name` / `description`; `disable-model-invocation: true` on the two
      that commit
- [x] `{REPO_ROOT}` removed from all four prompts
- [x] Automation drift check excised from `weekly-review-and-plan` (obsolete — no mirrors left)
- [x] Late-run guards added to `weekly-review-and-plan` and `daily-session-brief`
- [x] `CLAUDE.md` de-Coworked and now names the actual files — **it was untracked before this, so it
      is newly committed rather than modified**
- [x] `.claude/settings.json` — git allow-list narrowed to the exact paths the prompts may stage,
      plus a deny-list for `git add -A` / `git add .` / force-push / hard-reset
- [x] `.gitignore` — `.claude/settings.local.json`, `CLAUDE.local.md`
- [x] `automation/` retired; its README rewritten as `.claude/skills/README.md`
- [x] `STATUS.md` — open items harvested from Cowork auto-memory (§4.6)
- [x] `README.md` tree and assistant section updated

**Remaining (manual — can't be done from inside the repo)**

- [ ] Create the four stub files in `~/.claude/scheduled-tasks/` (§4.4), or ask Claude in a Desktop
      session to set them up
- [ ] Set schedule / folder / enabled state per the table in §5
- [ ] Copy the git allow rules into `~/.claude/settings.json` as well — the Desktop docs name that
      file specifically for scheduled-task sessions (§4.7, verification item 4)
- [ ] **Run now** on each task, choosing "always allow" for each prompt
- [ ] Diff and delete the stale dashboard artifact at
      `~/Documents/Claude/Artifacts/athlete-coach-dashboard/` (§4.5)
- [ ] Delete the Cowork memory files once `STATUS.md` is confirmed to cover them (§4.6)
- [ ] Work through §6 verification, then delete the old Cowork tasks
- [ ] Cosmetic: the now-empty `automation/` directory may still exist on disk — git doesn't track
      empty directories, so the commit is correct either way. `rmdir automation/tasks automation`

The step-by-step detail below is kept as the record of what was changed and why, and as the restore
reference for a future machine.

---

## 1. Where the task prompts should live

**Scheduled-task registrations cannot be committed.** Claude Code reads them only from
`~/.claude/scheduled-tasks/<task-name>/SKILL.md` (or under `CLAUDE_CONFIG_DIR`). There is no
project-scoped equivalent — the full inventory of committable `.claude/` files covers `CLAUDE.md`,
`rules/`, `settings.json`, `skills/`, `commands/`, `agents/`, `workflows/`, `output-styles/`,
`agent-memory/`, `.mcp.json`, and `.worktreeinclude`. Scheduled tasks are not on that list.

**But the prompt bodies can be, and should be.** Use a two-layer split:

| Layer | Path | In git | Holds |
|---|---|---|---|
| Prompt (the part that matters) | `.claude/skills/<name>/SKILL.md` | ✅ yes | The full instructions. Also invocable by hand as `/<name>`. |
| Registration (thin stub) | `~/.claude/scheduled-tasks/<name>/SKILL.md` | ❌ no | Two lines: "read the project skill and follow it". |
| Schedule / folder / model / enabled | Desktop Routines UI | ❌ no | Not stored in any file — documented in §5 below. |

So `.claude/skills/weekly-review-and-plan/SKILL.md` carries the real prompt, and the stub at
`~/.claude/scheduled-tasks/weekly-review-and-plan/SKILL.md` is:

```markdown
---
name: weekly-review-and-plan
description: Sunday weekly review for Denis + Alicja
---

Read `.claude/skills/weekly-review-and-plan/SKILL.md` in this project and follow it exactly.
```

### Why this is better than what we have now

- **The mirror-drift problem disappears.** Today `automation/tasks/*.md` are *copies* of the live
  prompts, kept in sync by a manual rule in `automation/README.md` ("whenever a live prompt is
  changed, update the mirror in the same session") plus an automation drift check inside the weekly
  review. With this layout the committed file **is** the live prompt. Both the maintenance rule and
  the drift check become dead weight — delete them (§4, step 6).
- **`{REPO_ROOT}` goes away.** Project skills run with the repo as the working folder, so relative
  paths (`people/denis/data.json`) just work. That removes the substitution step from every restore.
- **Same prompt, two entry points.** `/weekly-review-and-plan` in any session runs exactly what the
  Sunday schedule runs. Useful for the manual `start-training-block` especially.
- **Prompt changes become reviewable.** A change to how loads progress shows up as a normal diff.

### Trade-off

Four stub files still have to be created by hand on a new machine, and schedule/enabled state still
lives in the UI. That's a much smaller restore surface than today, and §5 documents it.

---

## 2. Inventory — what moves, what stays, what dies

| Thing | Currently | After | Action |
|---|---|---|---|
| Training state (`people/`, `shared/`) | in repo | unchanged | none |
| `CLAUDE.md` | in repo, works in both | in repo | **edit** — remove Cowork phrasing (§4.2) |
| Cowork project instructions ("AthleteTrainer") | Cowork project settings | `CLAUDE.md` | none — already byte-identical, so nothing is lost |
| 4 task prompts | live in Cowork + mirrored in `automation/tasks/` | `.claude/skills/<name>/SKILL.md` | **move** (§4.3) |
| Task registrations | Cowork scheduled tasks | `~/.claude/scheduled-tasks/` stubs | **recreate** (§4.4) |
| Dashboard | `tools/dashboard.html` (repo) **and** a stale Cowork artifact copy | repo only | **discard artifact** (§4.5) |
| Cowork auto-memory | `spaces/<id>/memory/*.md` | repo + Claude Code auto-memory | **harvest, then drop** (§4.6) |
| Tool permissions | per-task approvals in Cowork | `~/.claude/settings.json` + per-task allow | **recreate** (§4.7) |
| Dashboard GitHub token | browser `localStorage` per device | unchanged | none — independent of Claude |

---

## 3. Pre-flight

1. **Push outstanding work.** Auto-memory notes that commits `aa4ed17` / `5f45009` were local-only.
   Verify and resolve before restructuring:
   ```bash
   cd /Users/dandre/Projects/github.com/denisandreenko/athlete-training
   git status
   git log --oneline origin/main..HEAD
   git push
   ```
2. **Branch it.** `git checkout -b migrate-to-claude-code` — this touches automation wiring, and you
   want the option to walk it back.
3. **Install Claude Code Desktop** and trust this folder (Routines can't save a task against an
   untrusted folder).

---

## 4. Steps

### 4.1 Create the project config directory

```bash
mkdir -p .claude/skills
```

`.claude/settings.json` gets created in §4.7. Do **not** gitignore `.claude/` — most of it is meant
to be committed. Add only `.claude/settings.local.json` and `CLAUDE.local.md` to `.gitignore`.

### 4.2 Fix `CLAUDE.md`

Two problems with the current file:

- It opens with *"Use the uploaded context files as the source of truth"* — Cowork framing. There are
  no uploads in Claude Code; there's a repo.
- It never names the files, so every session has to rediscover them.

Replace that line with explicit paths, e.g.:

> Source of truth is this repo: `people/<id>/data.json` (structured state), the markdown files
> alongside it (plans, logs, skill state), and `shared/recommendation_protocol.md` (how
> recommendations are produced). Never rely on remembered values — read the files.

Keep the priority list and the answering rules exactly as they are; they work as-is. The file is well
under the 200-line / 25KB budget, so no need to split it into `.claude/rules/` yet. If it grows, `@path`
imports and `.claude/rules/*.md` (optionally path-gated) are the escape hatches.

### 4.3 Move the four prompts into `.claude/skills/`

For each of `daily-session-brief`, `weekly-review-and-plan`, `start-training-block`,
`monthly-nutrition-review`:

```bash
mkdir -p .claude/skills/<name>
git mv automation/tasks/<name>.md .claude/skills/<name>/SKILL.md
```

Then edit each `SKILL.md`:

1. **Rewrite the frontmatter.** Skills use `name` + `description` (both required); `allowed-tools` and
   `disable-model-invocation` are optional. The Cowork fields `taskId`, `cronExpression`, `enabled`,
   and `schedule` are not skill fields — move that information into the §5 table, or keep it as a
   comment in the body for reference.

   ```yaml
   ---
   name: weekly-review-and-plan
   description: Sunday weekly review for Denis and Alicja — assess the week, progress gym loads, calisthenics levels and cycling levels, maintain mesocycle counters, plan next week. Commits to data.json and calisthenics_status.md.
   ---
   ```

2. **Delete the `Repo root: {REPO_ROOT}` line.** Relative paths work. (`weekly-review-and-plan` has
   two occurrences.)

3. **Guard the read-only tasks against auto-invocation.** `daily-session-brief` and
   `monthly-nutrition-review` are harmless if they fire spontaneously mid-conversation. The two that
   write — `weekly-review-and-plan` and `start-training-block` — are not. Add to their frontmatter:

   ```yaml
   disable-model-invocation: true
   ```

   This keeps them out of automatic invocation while `/<name>` still works. **Verify this** in §6 —
   if an explicit `/name` inside a scheduled prompt turns out not to fire, fall back to the
   "read the file and follow it" stub wording shown in §1, which sidesteps invocation semantics
   entirely and is the recommended default anyway.

4. **Add a catch-up guardrail** to `weekly-review-and-plan` and `daily-session-brief`. Desktop starts
   one catch-up run for the most recent missed slot within a 7-day window, so a laptop that slept
   through Sunday 18:00 runs the review on Monday night. Both prompts reason about "the past 7 days"
   and "today's session", which quietly shifts. Add something like:

   > If the current time is more than 6 hours after the intended schedule (Sun 18:00), say so at the
   > top of the output and use the intended date as the reference point for the 7-day window, not the
   > current date.

`automation/tasks/` is now empty. Keep the directory only if you want `automation/README.md` to stay
where it is — see the next step.

### 4.4 Create the registration stubs

For each task, create `~/.claude/scheduled-tasks/<name>/SKILL.md` with `name` + `description`
frontmatter and a one-line body pointing at the project skill (template in §1).

Faster alternative: in a Desktop session, describe what you want in plain language — *"set up a
weekly task on Sunday at 6pm in the athlete-training folder that reads
`.claude/skills/weekly-review-and-plan/SKILL.md` and follows it"* — which creates the task, folder
binding, and schedule in one go. Then use the table in §5 to check each field.

### 4.5 Retire the dashboard artifact

There is a Cowork artifact copy of the dashboard at
`~/Documents/Claude/Artifacts/athlete-coach-dashboard/index.html`, last updated 2026-05-18. The repo's
`tools/dashboard.html` was updated 2026-07-20 and is 603 lines with the current person-switcher and
GitHub-API write path. **The repo file is canonical; the artifact is two months stale.** Diff them
once to confirm nothing unique is stranded, then delete the artifact directory.

The dashboard needs no migration: it's a static page that talks to the GitHub API with a token in
`localStorage`. Keep serving it however you do now (Pages or `open tools/dashboard.html`).

### 4.6 Harvest the Cowork memory, then let it go

Cowork memory lives at `spaces/26d21478-.../memory/` (`MEMORY.md`,
`user_athlete_dzianis.md`, `project_athlete_training.md`). Claude Code has auto-memory too, but it's
global-only at `~/.claude/projects/<project>/memory/` and not committable — so don't try to port it
directly. `automation/README.md` already says memory is "machine-local convenience only."

Almost all of it duplicates the repo. The exception is the **Pending** list, which exists nowhere in
git:

- Denis's FTP test is outstanding (`cycling.ftp` is `null`) — Zwift Ramp Test on a fresh day.
- Denis's structured block not yet started; rolling mesocycle covers deloads meanwhile.
- Alicja needs a GitHub token on her device to save log entries.

Land these in the repo — a `## Open items` section in `README.md`, or a `STATUS.md` — then delete the
memory files. Anything genuinely worth remembering, Claude Code will re-learn.

### 4.7 Permissions

`weekly-review-and-plan` and `start-training-block` run git and edit files unattended. Two mechanisms,
use both:

1. **Allow rules.** The Desktop docs specifically name `~/.claude/settings.json` as the file whose
   allow rules apply to scheduled-task sessions. Put the git allowances there rather than assuming
   project-scoped `.claude/settings.json` is picked up for scheduled runs — then confirm in §6.

   ```json
   {
     "permissions": {
       "allow": [
         "Bash(git status)",
         "Bash(git pull --rebase *)",
         "Bash(git add *)",
         "Bash(git commit *)",
         "Bash(git log *)",
         "Bash(git diff *)"
       ]
     }
   }
   ```

   The space before `*` matters: `Bash(git diff *)` works, `Bash(git diff*)` does not. Note that
   `Bash(git add *)` is broader than the repo's own rule — the prompts forbid `git add -A` / `git add .`
   and require staging by name. That constraint stays enforced by the prompt, not by permissions.
   Consider narrowing to the exact paths each task may stage.

2. **Per-task always-allow.** Click **Run now** on each task and select "always allow" on each prompt.
   Approvals persist per task and are revocable from the task's detail page. This is the direct
   equivalent of the existing instruction in `automation/README.md`.

Commit the project-scoped `.claude/settings.json` if you add non-secret settings there; keep personal
overrides in `.claude/settings.local.json` (gitignored).

### 4.8 Rewrite `automation/README.md`

It's a good document and mostly still true — the "workflow at a glance" and "key design rules"
sections carry real context. Update:

- **Restore procedure** — replace the `create_scheduled_task` / `{REPO_ROOT}` substitution steps with:
  create four stub files under `~/.claude/scheduled-tasks/`, set schedule and folder per the table,
  Run-now each one to pre-approve tools.
- **Delete the maintenance/mirror rule** — obsolete, there is no mirror anymore.
- **Point at `.claude/skills/`** as where the prompts live.
- Decide whether this file stays at `automation/README.md` or moves to `.claude/skills/README.md`
  next to the prompts. Recommend moving it; `automation/` then has no reason to exist.

Also remove the **automation drift check** from the `weekly-review-and-plan` prompt (§4.3) — it
compares live prompts against the mirrors, and there are none.

---

## 5. Registration reference (the part git can't hold)

Recreate exactly this in Routines → New routine → **Local**:

| Task | Schedule | Preset? | Enabled | Folder | Notes |
|---|---|---|---|---|---|
| `weekly-review-and-plan` | Sunday 18:00 | ✅ Weekly | **Active** | repo root | The engine; only scheduled task that commits |
| `daily-session-brief` | daily 07:45 | ✅ Daily | **Paused** | repo root | Activate when a training block starts |
| `start-training-block` | — | ✅ Manual | Active | repo root | Run by hand when the review flags 📦 Block-ready |
| `monthly-nutrition-review` | 1st Sunday, 19:00 | ❌ **no preset** | Active | repo root | Ask Claude in plain language: *"run this on the first Sunday of each month at 7pm"* |

Presets available are Manual, Hourly, Daily, Weekdays, Weekly. The monthly task's old cron
(`0 19 1-7 * 0`) has no preset equivalent, so it must be set conversationally.

Two operational notes carried over from Cowork:

- Tasks fire only while the Desktop app is open and the Mac is awake. Enable **Keep computer awake**
  (Settings → Desktop app → General) if the Sunday review matters. A closed lid still sleeps.
- Each run gets a small deterministic delay to stagger API traffic — the old Cowork tasks did the
  same (`jitterSeconds`), so the 18:00 review actually firing at 18:06 is expected, not a fault.

---

## 6. Verification

Do not consider the migration done until all of these pass:

1. **`/weekly-review-and-plan` works by hand** in a CLI session in the repo — confirms the skill is
   discovered and relative paths resolve without `{REPO_ROOT}`.
2. **Run now on `daily-session-brief`** (read-only, safest first test). It should produce a brief and
   touch nothing: `git status` clean afterwards.
3. **Run now on `weekly-review-and-plan`.** Approve tools as prompted with "always allow". Then check
   the diff — it must have staged *only* `data.json` / `calisthenics_status.md`, by name.
   ```bash
   git log -1 --stat
   ```
   If it staged anything else, the commit-scope instructions didn't survive the frontmatter rewrite.
4. **Confirm which settings file supplies allow rules** — if step 3 stalled on a git permission
   despite `~/.claude/settings.json`, the rules aren't being read; fix before trusting unattended runs.
5. **Verify `disable-model-invocation` didn't break scheduled invocation** (§4.3, item 3). If the
   scheduled run of a write-capable task does nothing, switch its stub to the "read the file and
   follow it" wording.
6. **Confirm the monthly schedule took.** Ask "show me my scheduled tasks" and check the next run date
   lands on the first Sunday of next month, not weekly.
7. **Dashboard still saves** — open `tools/dashboard.html`, log a test readiness entry, confirm the
   commit appears, then revert it.
8. **Sit through one real Sunday review** before deleting the Cowork tasks. Keep the old setup paused
   rather than deleted until then.

---

## 7. Rollback

Everything reversible: `git checkout main` restores the old layout, and the Cowork scheduled tasks
still exist (paused, not deleted) until step 8 above passes. The only irreversible acts are deleting
the stale dashboard artifact and the Cowork memory files — both are duplicates of repo content, and
§4.5 / §4.6 diff or harvest them first.

---

## Appendix A — launchd alternative

If depending on the Desktop app being open turns out to be the wrong trade, headless CLI on launchd
is the fallback. Sketch, not a recommendation:

```bash
cd /Users/dandre/Projects/github.com/denisandreenko/athlete-training
claude -p "Read .claude/skills/weekly-review-and-plan/SKILL.md and follow it exactly." \
  --permission-mode acceptEdits \
  --output-format json >> ~/Library/Logs/athlete-training/weekly.jsonl 2>&1
```

Wrap in a `launchd` plist with `StartCalendarInterval` (fires on wake if a run was missed, unlike
plain cron). Because the prompt bodies already live in `.claude/skills/`, switching to this path
requires no prompt changes — only the runner. Trade-offs versus Desktop: no interactive review of a
task that commits, permissions must be pre-granted more broadly (`--permission-mode` or
`--dangerously-skip-permissions`), and you own logging and failure alerting.

## Appendix B — things deliberately not changed

- **Cloud routines** were considered and rejected: they run from a fresh clone with no local file
  access, so commits would come from the cloud runner and the dashboard's browser→GitHub-API write
  path is outside their reach. Minimum interval is 1 hour, which would be fine; the file access is not.
- **Subagents.** `start-training-block` spawns an ad-hoc sports-science consultant subagent inline via
  its prompt. That keeps working. Promoting it to `.claude/agents/sports-science-consultant.md` (a
  committable, reusable definition with its own tools and model) is a reasonable follow-up, but it's a
  refactor, not a migration step.

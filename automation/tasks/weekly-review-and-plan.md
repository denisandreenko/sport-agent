---
taskId: weekly-review-and-plan
description: Sunday 18:00 weekly review for Denis + Alicja — assess the week, progress loads/phases, plan next week
cronExpression: "0 18 * * 0"
enabled: true
note: The engine of the workflow — the only task that commits on a schedule. Run once manually after restore to pre-approve tools.
---

You are a training assistant for two athletes: Dzianis (Denis) and Alicja. Perform the Sunday weekly review for BOTH, per shared/recommendation_protocol.md. Be direct and practical — use tables.

Repo root: {REPO_ROOT}

## Files to read
Shared: shared/recommendation_protocol.md, shared/training_principles.md
Per person (people/denis/ and people/alicja/): data.json (goals in priority order, weekly template, session targets, `mesocycle` state), workout_log.md (newest at bottom), training_plan.md. Denis extra: calisthenics_status.md (SKILL_STATE), gym_training_plan.md, the `cycling` section of data.json (FTP, zones, progression levels, phase), and training_block.md if an active block exists. Alicja extra: gym_training_plan.md (progression ladders), running_plan.md (phases), mobility_splits.md.

Extract each person's log entries from the past 7 days.

## Commit scope (important)
The ONLY files this task may edit: people/denis/calisthenics_status.md (skill level-ups) and either person's data.json — updating exercise `stub` starting loads or targets when progression is decided; the `mesocycle` object (advance/reset `week`, freeze on skips); and for Denis the `cycling` section: `cycling.levels` (ladder progression), `cycling.ftp` (only when he reports a new test result — move the old value to `history`), and `cycling.phase.current` (base/build rotation when due). Stage and commit ONLY the files you actually changed, by name — NEVER `git add -A` or `git add .`. Before committing, `git pull --rebase`. The written week-ahead plan is output in the conversation, not committed.

## Gap / return rule (check first, per person)
- 0 entries this week AND 0 the week before → output only a short return-week plan: resume at ~10–20% reduced loads/volume, reset mesocycle week to 1. Skip the detailed review for that person.
- 0 entries this week only → note the pause; next week resumes at the same loads (no progression, no punishment). Freeze the mesocycle counter (do not advance it). Never cram missed sessions.

## Mesocycle counter (per person, after the gap check)
Rules in each person's data.json `mesocycle.note`. Denis: 3+1 (deload every 4th completed week; paused entirely while training_block.md is active). Alicja: 5+1 (deload every 6th completed week).
- This week counted as completed (≥3 logged sessions) → advance `week` by 1 in data.json.
- Next week hits the deload number (Denis week 4, Alicja week 6) → NEXT WEEK IS THE DELOAD; plan it accordingly, then reset `week` to 1 after the deload week completes.
- Fatigue markers this week (2+ amber/red days, RPE creep at same loads, pain notes) → pull the deload forward to next week regardless of the counter, and reset the counter after it.
- Never postpone a due deload because the week "went well".

## Per-person review (do Denis first, then Alicja)

### Sessions completed
Table: Day | Planned (from data.json week) | Logged | RPE | Key note. Mark misses — don't reschedule them.

### Readiness & fatigue trend
Subjective ratings (sleep/soreness/energy/motivation, ≤2 = poor) and RPE across the week. Flag: 2+ amber/red days, RPE creeping at same loads, any pain notes. If ratings are missing most days, prompt (one line) to use the dashboard morning check-in.

### Progression
- Denis gym: per session, key compound loads vs prior week (↑/→/↓). Top of rep range hit at target RPE → "+load next session" and update the `stub` in data.json. No load progression into a deload week.
- Denis calisthenics: for skills worked this week, check exit criteria (data.json skills.ladders targets). If met with clean form → advance SKILL_STATE in calisthenics_status.md (status block + snapshot table) and note the next drill.
- Denis cycling (TrainerRoad-style, state in data.json `cycling`): per quality session (Tue VO2max, Thu threshold), check the logged session against the current ladder rung (`cycling.levels` → session `ladder`). All intervals completed at target power/RPE ≤ 8 → level +1 (update data.json); partial → hold; failed or 2+ week cycling gap → level −1. Only the phase-emphasized session progresses (`cycling.phase`: base → threshold ladder, build → VO2max ladder); the other holds as a maintenance dose. Rotate `phase.current` after 4–8 weeks in one phase (1–2 mesocycles). FTP retest flag: if FTP is null, is >8 weeks old, or interval power is up at same RPE/HR two weeks running, or the current threshold rung feels ≤ RPE 6 → recommend a Zwift Ramp Test this week (fresh day, not after Mon gym) instead of advancing further. When he reports a result, update `cycling.ftp` (old value to `history`). Guardrails respected (Mon→Tue, Fri→Sat)? Saturday outdoor ride is judged by HR/feel only — no power meter outdoors.
- Alicja gym: reps within range on all sets → add reps; top of range with 2+ RIR → small load increase or next ladder stage (gym_training_plan.md ladders). Technique first. No progression into a deload week.
- Alicja running: check phase criteria in running_plan.md (base wks 1–3 → threshold wks 4–7 → VO2max 8+). Recommend phase transition only if the current phase's sessions have felt easy and consistent. Fri stays easy if Thu gym left legs heavy. Running phases progress independently of the deload counter, but a deload week holds both runs at easy Z2.
- Alicja mobility: note any logged splits landmark progress.

## Block readiness (Denis only)
Only when NO training_block.md is active and next week is NOT a deload. Recommend starting a structured block when ALL hold:
- 3+ consecutive completed weeks (mesocycle history since the last deload/reset — a fresh post-deload week 1–2 does not qualify; the signal is a full clean mesocycle behind him)
- No pain notes and no red days in the past 2 weeks
- Loads/levels progressing or stable (not regressing)
- FTP tested and current (≤8 weeks old)
If all criteria pass, add ONE line to his section: "📦 Block-ready: last N weeks were clean and progressing — if the next 4 weeks are clear of travel/disruption, run start-training-block and enable the daily brief." List any single failed criterion in brackets instead (e.g. "[not block-ready: FTP untested]") only if 3 of 4 pass; otherwise say nothing.

## Independent review (subagent, Denis only, skip if his week was routine)
Spawn a subagent: "You are a sports science reviewer. Athlete: 87 kg male, ketogenic, training gravel cycling (priority 1) + strength/hypertrophy + calisthenics. Week's data: [paste his sessions + readiness/RPE trend]. Answer: (1) load appropriate/too high/too low? (2) adjustments for next week? 3–5 sentences, no questions." Incorporate; note disagreement.

## Next week plan (per person)
Table: Day | Session | Key focus | Load/intensity note. Rules:
- Deload week due (rolling counter, fatigue pull-forward, or week 4 of an active block) → plan it per the person's mesocycle.note: Denis gym volume −30–40%, cycling one rung below current level, long ride ~2 h Z1–Z2; Alicja gym −1 set at same loads, runs easy Z2, mobility kept in full. Label the plan "DELOAD WEEK".
- 2+ amber/red days or RPE creep → apply removal hierarchy; protect goal #1 (Denis: the long ride & cycling quality; Alicja: the two gym days)
- Pain flagged → hold load / regress a stage / check form
- Denis cycling rows: name the exact ladder rung (e.g. "Threshold L2: 3×15 min sweet spot") and watt targets if FTP is set; include a Ramp Test row if a retest was flagged
- Preserve the weekly template from data.json unless there's a reason to deviate; explain deviations in one line

## Output
Markdown, two clearly separated sections (Denis / Alicja), under ~700 words total. Show each person's mesocycle position (e.g. "Week 2 of 3+1 — deload in 2 weeks"). End with one sentence per person: the most important adjustment for next week and why.

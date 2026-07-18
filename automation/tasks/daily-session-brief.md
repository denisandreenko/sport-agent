---
taskId: daily-session-brief
description: Daily 07:45 session brief for Denis — today's workout with last loads, readiness call, and fueling
cronExpression: "45 7 * * *"
enabled: false
note: Enable when a training block starts (start-training-block reminds about this).
---

You are a training assistant for Dzianis (Denis). Generate today's session brief. Be concise and direct.

This is a READ-ONLY brief: do NOT edit, create, or commit any files. Just read and report.

Repo root: {REPO_ROOT}

## Files to read (in this order — per shared/recommendation_protocol.md)
1. people/denis/data.json — weekly template (`week`, keyed 0=Sun..6=Sat), session definitions with exercises/targets, `cycling` section (FTP, zones, progression levels, phase), nutrition fueling rules, supplements
2. shared/training_principles.md — readiness rule, removal hierarchy, deload
3. people/denis/workout_log.md — newest entries at the bottom
4. people/denis/training_plan.md — fatigue-stacking guardrails
5. people/denis/calisthenics_status.md — SKILL_STATE current levels (ladder definitions in data.json skills.ladders)
6. If a block is active (people/denis/training_block.md exists and today is within its date range): read it and use this week's targets instead of the defaults in data.json

## Step 1 — Today's session
Look up today's day-of-week in data.json `week` → session ID → definition in `sessions`.

## Step 2 — Readiness (subjective, from the log)
From the most recent log entries: today's (or latest) sleep / soreness / energy / motivation ratings (1–5; ≤2 = poor).
- 🟢 Green: 0 poor → train as planned
- 🟡 Amber: 1 poor → keep session, cut top-end volume ~20%, hold loads
- 🔴 Red: 2+ poor, or 2+ amber days running → easy/recovery only, apply removal hierarchy
If today's ratings aren't logged yet, ask in one line for them (or point to the dashboard check-in) and give the brief assuming green unless the recent trend (RPE creep, pain notes, amber days) says otherwise.

## Step 3 — Skip/pause awareness
If the last 7+ days have no log entries, do NOT output a normal brief. Output one short paragraph: acknowledge the gap, suggest a light re-entry session, and recommend waiting for the Sunday weekly review to rebuild the week. Never suggest cramming missed sessions.

## Step 4 — Output the brief

**[Weekday] — [Session label]**
*[Date]*

### Readiness
One line: 🟢/🟡/🔴 with the ratings it's based on and what it means for today.

### Today's plan
GYM: table — Exercise | Target | Last load (most recent same-session entry in the log; else the `stub` from data.json). Apply amber/red trim. Note deload if week 4 of an active block. Include the session `note` (activation) and `mobility` line from data.json.
CYCLING: purpose + the exact ladder rung for today from data.json — session `ladder` at the current level in `cycling.levels`, with watt targets from `cycling.ftp` × `cycling.zones` (if FTP is null, give RPE targets and note the pending Ramp Test). On amber, hold the rung but cut 1 interval; on red, easy spin only. Include the `prep` line and the fueling rule (TKD carbs for VO2max/threshold, from data.json nutrition.fueling). Respect the fatigue-stacking guardrails (Mon squat→Tue VO2max; Fri hinge→Sat long ride). Saturday long ride: HR/feel only, no power targets.
REST: short recovery checklist.

### Skill add-on (gym days only)
Use the `addon` line from today's session in data.json plus current levels from SKILL_STATE. Name the specific drill at the CURRENT level and the target to hit before leveling up (from data.json skills.ladders). 10–15 min, low-fatigue, technical, never to failure.

### Pre-session supplements
From data.json nutrition.supplements: only rows whose timing is pre-gym / pre-endurance / pre-calisthenics. Add TKD carbs line if today is hard cycling.

End with one sentence: the single most important thing to execute well today.

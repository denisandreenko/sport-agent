---
name: start-training-block
description: Build Denis a 4-week periodized training block and write it to people/denis/training_block.md. Run this only when explicitly asked by name — it commits four weeks of calendar.
disable-model-invocation: true
---

<!-- Scheduled: Manual only. Deliberate overload phase — run when the Sunday review flags
     "📦 Block-ready" and the next 4 weeks are clear of travel/disruption. Suspends the rolling
     mesocycle counter while training_block.md is active. See .claude/skills/README.md. -->

You are a training assistant for Dzianis (Denis, 87 kg, ~11% BF, ketogenic, ex-triathlete now training gravel cycling (priority 1) + strength/hypertrophy + calisthenics). Build a complete 4-week periodized training block and save it to the repo.

All paths below are relative to the repository root, which is the working folder for this session.

## Step 1 — Read all context
- people/denis/data.json — goals, weekly template, session definitions with exercise targets and `stub` starting loads, skills.ladders, `cycling` section (FTP, zones, ladder levels, phase), nutrition fueling rules
- shared/recommendation_protocol.md and shared/training_principles.md
- people/denis/training_plan.md (fatigue-stacking guardrails, periodization rules) and gym_training_plan.md (progression rules)
- people/denis/calisthenics_status.md — SKILL_STATE current levels and primary-skill focus
- people/denis/workout_log.md — baseline loads for all logged exercises, recent readiness/RPE trend

## Commit scope (important)
This task creates people/denis/training_block.md and edits people/denis/profile.md (Training Block Status) — nothing else. `git add` ONLY those two files by name; NEVER `git add -A` or `git add .`. `git pull --rebase` before committing.

## Step 2 — Research (2 targeted searches)
1. Concurrent strength + endurance periodization for a trained athlete (recent evidence).
2. Calisthenics skill acquisition frequency alongside strength training (motor learning).
Summarise each in 2–3 sentences; let findings inform the design.

## Step 3 — Independent review via subagent
Spawn a subagent: "You are an independent sports science consultant. Athlete: male, 87 kg, ~11% BF, ketogenic, ex-triathlete; goals: (1) gravel cycling, (2) strength/hypertrophy, (3) calisthenics skills, (4) mobility. Capacity: gym 3×/wk ~1 h, cycling quality 2×/wk, long ride Saturday, calisthenics skill work 3×/wk 10–15 min before lifting. No races planned. Current primary skills: [read from calisthenics_status.md SKILL_STATE]. Propose 5–8 concrete periodization principles for a 4-week block: volume distribution, intensity progression, deload structure, and balancing cycling quality with gym legs. No questions." Incorporate; note disagreements.

## Step 4 — Build the block
Structure: Wk1 baseline (establish loads @ RPE 7) → Wk2 accumulation (+1 set key accessories, hold compounds) → Wk3 intensification (+2.5–5 kg on compounds where rep range was hit; accessories to top of range) → Wk4 deload (volume −30–40%, keep some intensity, prioritize mobility/sleep).

Per week output:
- Table: Day | Session | Key focus | Intensity target | Notes (base it on data.json `week`; respect Mon→Tue and Fri→Sat guardrails)
- Gym load tables: Exercise | Wk1 | Wk2 | Wk3 | Wk4 — Wk1 from last logged loads (else data.json `stub`)
- Cycling: interval targets per week from the current ladder rung in data.json `cycling` (progressing volume along the ladder, watt targets from FTP × zones; RPE if FTP is null)
- Calisthenics: per primary skill, drill + weekly progression using CURRENT SKILL_STATE levels and the per-level targets in shared/calisthenics_ladders.md
- Fueling: which sessions need TKD carbs (data.json nutrition.fueling); calorie note for Wk2–3. Reference only — do NOT edit nutrition data.

## Step 5 — Save and update status
Write the block to people/denis/training_block.md with block start date (today), end date (+28 days), deload week dates, and the key principles from Steps 2–3 at the top. Edit people/denis/profile.md Training Block Status to "Block started: [date]. Week 1 of 4. Deload week: [date]." Commit both per the commit-scope rule.

## Step 6 — Output in conversation
Confirm saved. Show: Week 1 seven-day table, top 3 focus points, one nutrition-alignment reminder. Finish by reminding Dzianis to enable the daily-session-brief scheduled task now that the block is live.

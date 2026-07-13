#!/usr/bin/env python3
"""
Strava → workout_log.md auto-sync
Runs nightly via GitHub Actions. Fetches activities from the last 36 hours,
maps them to the workout_log.md format, and prepends new entries.
Skips dates that already have an entry of the same session type.
"""

import os
import sys
from datetime import datetime, timezone, timedelta

import requests

# ── Config ────────────────────────────────────────────────────────────────────
CLIENT_ID     = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]
LOG_FILE      = "people/denis/workout_log.md"

# ── Day-of-week → default cycling session type (weekday() 0=Monday) ──────────
CYCLING_BY_DOW = {
    1: "CYCLING_VO2MAX",    # Tuesday
    3: "CYCLING_THRESHOLD", # Thursday
    5: "CYCLING_LONG",      # Saturday
}

RUN_BY_DOW = {
    1: "RUN_VO2MAX",
    3: "RUN_THRESHOLD",
    5: "RUN_LONG",
}

# ── Strava sport type → category ──────────────────────────────────────────────
SPORT_CATEGORY = {
    "Ride":              "cycling",
    "VirtualRide":       "cycling",
    "GravelRide":        "cycling",
    "MountainBikeRide":  "cycling",
    "Run":               "run",
    "TrailRun":          "run",
    "Swim":              "swim",
}

# ── Strava API ─────────────────────────────────────────────────────────────────
def get_access_token():
    resp = requests.post("https://www.strava.com/oauth/token", json={
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type":    "refresh_token",
    }, timeout=15)
    if resp.status_code != 200:
        print(f"::error::Strava token refresh failed ({resp.status_code}): {resp.text}")
        print("::error::The STRAVA_REFRESH_TOKEN secret is likely stale (Strava rotates "
              "refresh tokens). Re-authorize and update the repo secret — see README.")
        sys.exit(1)
    data = resp.json()
    # Strava rotates refresh tokens. If a new one is issued, surface it in the job log
    # (masked secrets aren't echoed; the token itself is safe to print only in a private repo,
    # so we just warn — update the secret from https://www.strava.com/settings/api flow).
    if data.get("refresh_token") and data["refresh_token"] != REFRESH_TOKEN:
        print("::warning::Strava issued a NEW refresh token. Update the STRAVA_REFRESH_TOKEN "
              "secret soon or future runs will fail.")
    return data["access_token"]


def get_recent_activities(token):
    # Default window 36 h; set SYNC_HOURS when dispatching manually to backfill a gap.
    hours = int(os.environ.get("SYNC_HOURS", "36"))
    after = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp())
    resp = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {token}"},
        params={"after": after, "per_page": 15},
        timeout=15,
    )
    if resp.status_code == 403:
        print(f"::error::Strava returned 403 for /athlete/activities: {resp.text}")
        print("::error::The token refreshed OK but lacks the activity:read_all scope. "
              "Re-authorize with scope=read,activity:read_all and update the "
              "STRAVA_REFRESH_TOKEN secret.")
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


# ── Session type determination ─────────────────────────────────────────────────
def determine_session_type(activity, dow):
    category = SPORT_CATEGORY.get(activity["type"])
    if not category:
        return None

    name = activity["name"].lower()
    is_indoor = activity["type"] == "VirtualRide" or activity.get("trainer", False)

    if category == "cycling":
        if is_indoor:
            # Indoor trainer — use day default, fall back to threshold
            return CYCLING_BY_DOW.get(dow, "CYCLING_THRESHOLD")
        # Outdoor — use day default, fall back to CYCLING_LONG
        return CYCLING_BY_DOW.get(dow, "CYCLING_LONG")

    if category == "run":
        # Try to infer from activity name
        if any(k in name for k in ("vo2", "interval", "repeat", "track", "hiit")):
            return "RUN_VO2MAX"
        if any(k in name for k in ("threshold", "tempo", "t-pace")):
            return "RUN_THRESHOLD"
        if any(k in name for k in ("long", "easy", "recovery", "base")):
            return "RUN_LONG"
        return RUN_BY_DOW.get(dow, "RUN_THRESHOLD")

    if category == "swim":
        return "SWIM"

    return None


# ── Formatting helpers ─────────────────────────────────────────────────────────
def fmt_duration(seconds):
    return f"{seconds // 60}min"


def fmt_pace_or_power(activity):
    category = SPORT_CATEGORY.get(activity["type"], "")
    if category == "cycling":
        watts = activity.get("average_watts")
        if watts and watts > 0:
            return f"{int(watts)}W"
        spd = activity.get("average_speed", 0)
        return f"{spd * 3.6:.1f}km/h" if spd > 0 else None
    if category == "run":
        spd = activity.get("average_speed", 0)
        if spd > 0:
            spm = 1000 / spd
            return f"{int(spm // 60)}:{int(spm % 60):02d}/km"
    if category == "swim":
        spd = activity.get("average_speed", 0)
        if spd > 0:
            spm = 100 / spd
            return f"{int(spm // 60)}:{int(spm % 60):02d}/100m"
    return None


def fmt_terrain(activity):
    if activity["type"] == "VirtualRide" or activity.get("trainer", False):
        return "trainer"
    category = SPORT_CATEGORY.get(activity["type"], "")
    name = activity["name"].lower()
    if category == "cycling":
        if any(k in name for k in ("gravel", "dirt", "trail", "mtb", "off-road")):
            return "gravel"
        return "road"
    if category == "run":
        return "trail" if any(k in name for k in ("trail", "gravel", "mountain")) else "road"
    if category == "swim":
        return "pool"
    return None


# ── Entry builder ──────────────────────────────────────────────────────────────
def build_entry(activity, date_str, session_type):
    dist_km   = activity.get("distance", 0) / 1000
    elev      = activity.get("total_elevation_gain", 0)
    avg_hr    = activity.get("average_heartrate")
    max_hr    = activity.get("max_heartrate")
    act_name  = activity["name"]

    # Notes line
    parts = [f'Auto-synced from Strava: "{act_name}"']
    if dist_km > 0.1:
        parts.append(f"{dist_km:.1f}km")
    if elev > 5:
        parts.append(f"{int(elev)}m gain")
    if avg_hr:
        parts.append(f"avg HR {int(avg_hr)}")
    if max_hr:
        parts.append(f"max HR {int(max_hr)}")

    # Subjective readiness/RPE are unknown for auto-synced entries — omit rather than
    # write placeholders (per the workout_log FORMAT SPEC). Denis adds them via dashboard.
    lines = [
        f"## {date_str} | {session_type}",
        f"- notes: {' · '.join(parts)}",
        f"",
        f"### Endurance",
        f"- duration: {fmt_duration(activity.get('moving_time', 0))}",
    ]

    pp = fmt_pace_or_power(activity)
    if pp:
        lines.append(f"- avg_power_or_pace: {pp}")

    terrain = fmt_terrain(activity)
    if terrain:
        lines.append(f"- terrain: {terrain}")

    return "\n".join(lines)


# ── Log file helpers ──────────────────────────────────────────────────────────
def entry_exists(content, date_str, session_type):
    return f"## {date_str} | {session_type}" in content


def append_entry(content, entry):
    """Append at the end — the log is chronological, newest at the bottom
    (same convention as the dashboard and the weekly review)."""
    return content.rstrip() + "\n\n" + entry + "\n\n---\n"


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("Fetching Strava access token...")
    token = get_access_token()

    print(f"Fetching recent activities (last {os.environ.get('SYNC_HOURS', '36')} h)...")
    activities = get_recent_activities(token)
    print(f"  → {len(activities)} activit{'y' if len(activities) == 1 else 'ies'} found")

    if not activities:
        print("Nothing to sync.")
        return

    with open(LOG_FILE, "r") as f:
        content = f.read()

    added = 0
    for act in activities:
        # start_date_local is already in athlete's local time (e.g. "2026-05-20T09:30:00Z")
        local_str = act["start_date_local"]
        date_str  = local_str[:10]
        dow       = datetime.fromisoformat(local_str).weekday()  # 0=Monday

        category = SPORT_CATEGORY.get(act["type"])
        if not category:
            print(f"  Skip: {act['type']} '{act['name']}' (not a tracked sport)")
            continue

        session_type = determine_session_type(act, dow)
        if not session_type:
            print(f"  Skip: could not map '{act['name']}' to a session type")
            continue

        if entry_exists(content, date_str, session_type):
            print(f"  Skip: entry already exists for {date_str} | {session_type}")
            continue

        print(f"  Add: {date_str} | {session_type} — {act['name']}")
        content = append_entry(content, build_entry(act, date_str, session_type))
        added += 1

    if added > 0:
        with open(LOG_FILE, "w") as f:
            f.write(content)
        print(f"\nDone — {added} new entr{'y' if added == 1 else 'ies'} written to {LOG_FILE}")
    else:
        print("\nDone — no new entries.")


if __name__ == "__main__":
    main()

"""Actions minutes guard: billable estimation, projection, throttle
decisions, skip cadence, cron rewriting, alert wording. Pure parts only."""

from datetime import datetime, timezone

from tipoff import (
    CADENCE_CRON, CFG, budget_outlook, decide_eco_n,
    estimate_billable_minutes, format_budget_alert, format_daily_ping,
    month_context, set_cron_cadence, should_skip_run,
)


def ts_utc(y, mo, d, h=12):
    return datetime(y, mo, d, h, tzinfo=timezone.utc).timestamp()


# --- month context -------------------------------------------------------------

def test_month_context_midmonth():
    ym, start, frac = month_context(ts_utc(2026, 7, 16, 0))
    assert ym == "2026-07" and start == "2026-07-01"
    assert abs(frac - 15 / 31) < 0.01


def test_month_context_december_rollover():
    ym, start, frac = month_context(ts_utc(2026, 12, 31, 23))
    assert ym == "2026-12" and frac > 0.96


# --- billable estimation ---------------------------------------------------------

def run_record(minutes):
    start = datetime(2026, 7, 10, 12, 0, tzinfo=timezone.utc)
    end = datetime(2026, 7, 10, 12, 0, tzinfo=timezone.utc).timestamp() + minutes * 60
    return {"run_started_at": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated_at": datetime.fromtimestamp(end, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ")}


def test_billable_rounds_up_per_run():
    # 1.2 min + 0.5 min bill as 2 + 1, not 1.7
    assert estimate_billable_minutes([run_record(1.2), run_record(0.5)]) == 3.0


def test_billable_one_minute_floor():
    assert estimate_billable_minutes([run_record(0.1)]) == 1.0


def test_billable_skips_malformed_records():
    assert estimate_billable_minutes([{"run_started_at": ""}]) == 0.0


# --- projection ------------------------------------------------------------------

def test_outlook_projects_straight_line():
    # 600 min used halfway through the month -> 1200 projected
    o = budget_outlook(600, 1800, month_frac=0.5)
    assert abs(o["projected"] - 1200) < 1e-6
    assert abs(o["used_pct"] - 1 / 3) < 1e-6


def test_outlook_damps_day_one_noise():
    # 30 min in the first hour of the month must not project 20,000+
    o = budget_outlook(30, 1800, month_frac=0.001)
    assert o["projected"] <= 30 / (CFG["BUDGET_MIN_ELAPSED_DAYS"] / 31.0) + 1


# --- throttle decision --------------------------------------------------------------

def outlook(used_pct=0.3, projected_pct=0.5):
    return {"used": used_pct * 1800, "budget": 1800, "used_pct": used_pct,
            "projected": projected_pct * 1800, "projected_pct": projected_pct}


def test_decide_stays_hourly_inside_budget():
    assert decide_eco_n(outlook(projected_pct=0.90)) == 1


def test_decide_downshifts_on_projection():
    assert decide_eco_n(outlook(projected_pct=1.0)) == 2
    assert decide_eco_n(outlook(projected_pct=1.5)) == 3
    assert decide_eco_n(outlook(projected_pct=2.5)) == 6


def test_decide_hard_brake_when_nearly_empty():
    assert decide_eco_n(outlook(used_pct=0.96, projected_pct=1.0)) == 6


def test_decide_never_speeds_up_within_month():
    # projection improved, but we already throttled: hold at 3
    assert decide_eco_n(outlook(projected_pct=0.5), current_n=3) == 3


# --- skip cadence ---------------------------------------------------------------------

def test_skip_hourly_never_skips():
    assert not any(should_skip_run(1, h) for h in range(24))


def test_skip_preserves_ping_hour():
    for n in (2, 3, 6):
        assert not should_skip_run(n, CFG["PING_UTC_HOUR"])


def test_skip_every_other_hour_at_n2():
    ran = [h for h in range(24) if not should_skip_run(2, h)]
    assert len(ran) == 12
    assert CFG["PING_UTC_HOUR"] in ran


def test_skip_n6_runs_four_times_a_day():
    ran = [h for h in range(24) if not should_skip_run(6, h)]
    assert len(ran) == 4


# --- cron rewriting -----------------------------------------------------------------

WORKFLOW_SNIPPET = '''on:
  schedule:
    # Hourly, at :07 — GitHub delays top-of-the-hour crons heavily.
    - cron: "7 * * * *"
  workflow_dispatch: {}
'''


def test_set_cron_cadence_rewrites_only_cron_line():
    out = set_cron_cadence(WORKFLOW_SNIPPET, 2)
    assert '- cron: "7 */2 * * *"' in out
    assert "workflow_dispatch" in out
    assert out.count("cron:") == WORKFLOW_SNIPPET.count("cron:")


def test_set_cron_cadence_roundtrip_back_to_hourly():
    slowed = set_cron_cadence(WORKFLOW_SNIPPET, 6)
    restored = set_cron_cadence(slowed, 1)
    assert f'- cron: "{CADENCE_CRON[1]}"' in restored


# --- alert wording ------------------------------------------------------------------

def test_budget_alert_cron_mode():
    msg = format_budget_alert(outlook(used_pct=0.82, projected_pct=1.1), 2, "cron")
    assert msg.startswith("⛽ Tipoff minutes check")
    assert "1,476/1,800" in msg and "(82%)" in msg
    assert "rewrote my own cron to every 2h" in msg


def test_budget_alert_skip_mode_mentions_pat():
    msg = format_budget_alert(outlook(), 2, "skip")
    assert "skipping" in msg and "WORKFLOW_EDIT_TOKEN" in msg


def test_budget_alert_warn_only():
    msg = format_budget_alert(outlook(used_pct=0.81), 1, "warn")
    assert "No throttle change" in msg


# --- ping integration ---------------------------------------------------------------

def test_ping_includes_minutes_line_when_known():
    stats = {"runs": 24, "markets": 1650, "alerts": 0, "watches": 7,
             "open_positions": 0, "graded": 0, "wins": 0, "losses": 0,
             "avg_clv": 0.0, "calib_day": 0,
             "minutes_used": 412, "minutes_budget": 1800,
             "minutes_pct": 412 / 1800, "cadence": "hourly"}
    msg = format_daily_ping(stats)
    assert "⛽ 412/1,800 Actions min (23%) · hourly" in msg


def test_ping_omits_minutes_line_when_unknown():
    stats = {"runs": 24, "markets": 1650, "alerts": 0, "watches": 7,
             "open_positions": 0, "graded": 0, "wins": 0, "losses": 0,
             "avg_clv": 0.0, "calib_day": 0}
    assert "⛽" not in format_daily_ping(stats)

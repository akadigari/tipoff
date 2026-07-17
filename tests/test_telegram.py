"""Telegram formatters: exact alert header, one fact per line, daily ping,
ping scheduling. All pure, no network."""

from datetime import datetime, timezone

from tipoff import ALERT_HEADER, CFG, format_alert, format_daily_ping, should_ping


def alert(**overrides):
    base = {
        "title": "Will the Fed cut rates in September?",
        "platform": "kalshi",
        "market_id": "KXFED-25SEP-C",
        "signals": ["volume spike (12x baseline)",
                    "price jump +9c in 1.0h"],
        "side": "yes",
        "entry_price": 0.62,
        "category": "politics",
        "stake_usd": 50.0,
        "hours_to_close": 30.0,
        "score": 72,
        "url": "",
    }
    base.update(overrides)
    return base


def test_header_is_exact_and_leads():
    msg = format_alert(alert())
    assert msg.splitlines()[0] == "🚨🚨 ALERT!!! INSIDER TRADING SCOOP 🚨🚨"
    assert msg.splitlines()[0] == ALERT_HEADER


def test_required_facts_each_on_own_line():
    lines = format_alert(alert()).splitlines()
    assert any("Will the Fed cut rates" in ln for ln in lines)
    assert any(ln.startswith("🔔 Signal:") and "volume spike" in ln
               and "price jump" in ln for ln in lines)
    assert any(ln.startswith("💵 Price: 62c") for ln in lines)
    assert any(ln.startswith("🏷 Category: politics") for ln in lines)
    assert any(ln.startswith("📐 Suggested size: $50") for ln in lines)
    assert any("Window open: verify + move." in ln for ln in lines)


def test_side_is_explicit():
    assert "buy YES" in format_alert(alert(side="yes"))
    assert "buy NO" in format_alert(alert(side="no"))


def test_resolve_window_formats_hours_and_days():
    assert "resolves in 30h" in format_alert(alert(hours_to_close=30.0))
    assert "resolves in 5d" in format_alert(alert(hours_to_close=120.0))


def test_url_included_only_when_present():
    assert "🔗" not in format_alert(alert(url=""))
    msg = format_alert(alert(url="https://polymarket.com/event/foo"))
    assert "🔗 https://polymarket.com/event/foo" in msg.splitlines()


def test_calibration_footer_only_during_calibration():
    assert "calibration week" not in format_alert(alert())
    assert "calibration week" in format_alert(alert(calib=True))


def test_fits_single_telegram_message():
    long_title = "W" * 300
    msg = format_alert(alert(title=long_title,
                             signals=["volume spike (99x baseline)"] * 5))
    assert len(msg) < 4096  # Telegram sendMessage hard limit


# --- daily ping -----------------------------------------------------------------

def ping_stats(**overrides):
    base = {"runs": 24, "markets": 1650, "alerts": 0, "watches": 7,
            "open_positions": 0, "graded": 0, "wins": 0, "losses": 0,
            "avg_clv": 0.0, "calib_day": 0}
    base.update(overrides)
    return base


def test_ping_quiet_day():
    msg = format_daily_ping(ping_stats())
    assert msg.splitlines()[0].startswith("🟢 Tipoff daily check-in")
    assert "24 scans" in msg and "1,650 markets" in msg
    assert "0 alerts" in msg and "7 watches" in msg
    assert "All quiet" in msg


def test_ping_active_day_with_book():
    msg = format_daily_ping(ping_stats(alerts=2, graded=5, wins=3, losses=2,
                                       open_positions=4, avg_clv=0.012))
    assert "2 alerts" in msg
    assert "5 graded (3W-2L, avg CLV +1.2c)" in msg
    assert "All quiet" not in msg


def test_ping_mentions_calibration_week():
    msg = format_daily_ping(ping_stats(calib_day=3))
    assert "calibration week: day 3/7" in msg
    assert "watch log" in msg


def test_ping_open_positions_without_grades():
    msg = format_daily_ping(ping_stats(open_positions=2))
    assert "2 open, none resolved yet" in msg


# --- ping scheduling ---------------------------------------------------------------

def ts_at_utc_hour(hour):
    return datetime(2026, 7, 15, hour, 10, tzinfo=timezone.utc).timestamp()


def test_ping_fires_at_target_hour_after_min_gap():
    ts = ts_at_utc_hour(CFG["PING_UTC_HOUR"])
    meta = {"last_ping_ts": ts - 24 * 3600}
    assert should_ping(meta, ts)


def test_ping_skips_other_hours_within_max_gap():
    ts = ts_at_utc_hour((CFG["PING_UTC_HOUR"] + 3) % 24)
    meta = {"last_ping_ts": ts - 24 * 3600}
    assert not should_ping(meta, ts)


def test_ping_no_double_send_same_day():
    ts = ts_at_utc_hour(CFG["PING_UTC_HOUR"])
    meta = {"last_ping_ts": ts - 3600}  # pinged an hour ago
    assert not should_ping(meta, ts)


def test_ping_fallback_after_max_gap():
    ts = ts_at_utc_hour((CFG["PING_UTC_HOUR"] + 5) % 24)
    meta = {"last_ping_ts": ts - CFG["PING_MAX_GAP_H"] * 3600 - 1}
    assert should_ping(meta, ts)


def test_ping_fires_on_very_first_run():
    assert should_ping({}, ts_at_utc_hour(2))  # hello ping, any hour

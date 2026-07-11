"""Research dataset: forward-return filling and row construction — the data
that later answers 'which signals actually predict moves'."""

from tipoff import (
    RESEARCH_COLUMNS, RESEARCH_GRACE_H, fill_forward_returns, format_daily_ping,
    research_row,
)

NOW = 1_780_000_000.0
H = 3600.0


def row(age_hours, platform="kalshi", market_id="M1", **overrides):
    base = {
        "platform": platform, "market_id": market_id,
        "ts_unix": f"{NOW - age_hours * H:.0f}",
        "p_1h": "", "p_6h": "", "p_24h": "",
    }
    base.update(overrides)
    return base


def test_fills_due_horizons_only():
    r = row(age_hours=2)  # 1h due, 6h/24h not yet
    filled = fill_forward_returns([r], {"kalshi:M1": 0.61}, NOW)
    assert filled == 1
    assert r["p_1h"] == "0.6100" and r["p_6h"] == "" and r["p_24h"] == ""


def test_fills_all_when_old_enough():
    r = row(age_hours=30)
    filled = fill_forward_returns([r], {"kalshi:M1": 0.70}, NOW)
    assert filled == 3
    assert r["p_1h"] == r["p_6h"] == r["p_24h"] == "0.7000"


def test_never_overwrites_existing_fill():
    # p_1h was captured an hour after the signal; a later pass must not
    # replace it with today's price
    r = row(age_hours=30, p_1h="0.5500")
    fill_forward_returns([r], {"kalshi:M1": 0.90}, NOW)
    assert r["p_1h"] == "0.5500"
    assert r["p_6h"] == "0.9000"


def test_missing_market_waits_through_grace_then_na():
    r = row(age_hours=1.5)  # 1h due 0.5h ago; grace is 6h
    filled = fill_forward_returns([r], {}, NOW)
    assert filled == 0 and r["p_1h"] == ""
    r2 = row(age_hours=1 + RESEARCH_GRACE_H + 0.1)
    filled = fill_forward_returns([r2], {}, NOW)
    assert r2["p_1h"] == "na" and filled == 1


def test_row_shape_matches_columns():
    cand = {
        "platform": "poly", "id": "0xabc", "title": "T", "category": "crypto",
        "price": 0.42, "vol24": 8000.0,
        "signals": [{"type": "large_trade", "desc": "$3,000 single trade",
                     "points": 12, "wallet": "0xwallet"},
                    {"type": "thin_market", "desc": "thin", "points": 10}],
    }
    r = research_row(cand, NOW, "calib", True, 62, "yes", 0.44, 2500.0,
                     48.0, [])
    assert set(r) == set(RESEARCH_COLUMNS)
    assert r["alerted"] == "1" and r["wallet"] == "0xwallet"
    assert r["yes_price"] == "0.4200" and r["mode"] == "calib"


def test_row_without_large_trade_has_no_wallet():
    cand = {"platform": "kalshi", "id": "K1", "title": "T",
            "category": "politics", "price": 0.60, "vol24": 50000.0,
            "signals": [{"type": "price_jump", "desc": "jump", "points": 20,
                         "direction": 1}]}
    r = research_row(cand, NOW, "normal", False, 20, "yes", 0.61, 900.0,
                     30.0, ["score 20 < 55"])
    assert r["wallet"] == "" and r["alerted"] == "0"
    assert r["gate_reasons"] == "score 20 < 55"


# --- health line in the daily ping -------------------------------------------

def ping_stats(**overrides):
    base = {"runs": 24, "markets": 1650, "alerts": 0, "watches": 7,
            "open_positions": 0, "graded": 0, "wins": 0, "losses": 0,
            "avg_clv": 0.0, "calib_day": 0, "errors": 2,
            "health": {"kalshi": 1175, "poly": 476, "warm": 1540}}
    base.update(overrides)
    return base


def test_ping_health_line():
    msg = format_daily_ping(ping_stats())
    assert "🩺 kalshi 1,175 ✓ · poly 476 ✓ · 1,540 baselines warm" in msg
    assert "2 fetch errors (24h)" in msg


def test_ping_health_flags_dead_platform():
    msg = format_daily_ping(ping_stats(
        health={"kalshi": 1175, "poly": 0, "warm": 900}))
    assert "poly 0 ⚠️" in msg


def test_ping_no_health_line_when_unknown():
    msg = format_daily_ping(ping_stats(health=None))
    assert "🩺" not in msg

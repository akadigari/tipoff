"""Fixes driven by the insider-episode backtest (docs/BACKTEST.md): every
test here encodes a failure mode observed replaying a documented episode."""

from tipoff import (
    CFG, MONITOR_HEADER, choose_side, detect_price_jump, detect_volume_spike,
    followability_gate, format_alert, hours_until_close, is_insider_archetype,
    wallet_age_from_name,
)

NOW = 1_780_000_000.0


def obs(dp=0.0, p_prev=0.50, rate=100.0, dv_usd=1000.0, n=20, dt_h=1.0):
    return {"dt_h": dt_h, "rate": rate, "dp": dp, "dv": rate * dt_h,
            "dv_usd": dv_usd, "p_prev": p_prev, "impact": None,
            "base_impact": 0.0, "base_mean": 100.0,
            "n": n, "recent_moves": [0.01] * 8}


# --- Nobel fix: extreme repricings bypass the scheduled-news proxy ----------

def test_extreme_dp_fires_inside_news_window():
    # 3.7c -> 39c longshot repricing 2h before close (the Nobel leak shape)
    sig = detect_price_jump(obs(dp=0.353, p_prev=0.037), hours_to_close=2.0)
    assert sig is not None and sig["direction"] == 1


def test_extreme_odds_ratio_fires_inside_news_window():
    # 2c -> 12c is only a 10c move but a 6x odds change
    sig = detect_price_jump(obs(dp=0.10, p_prev=0.02), hours_to_close=2.0)
    assert sig is not None


def test_ordinary_jump_still_suppressed_near_close():
    # 50c -> 62c the hour before a game ends is the event, not a leak
    assert detect_price_jump(obs(dp=0.12), hours_to_close=2.0) is None


# --- Iran fix: unknown clock must not suppress ------------------------------

def test_unknown_close_does_not_suppress_jump():
    assert detect_price_jump(obs(dp=0.08), hours_to_close=None) is not None


def test_hours_until_close_stale_clock_is_none():
    # gamma endDate a month in the past on an ACTIVE market
    assert hours_until_close({"close_ts": NOW - 30 * 86400}, NOW) is None
    assert hours_until_close({"close_ts": None}, NOW) is None
    assert abs(hours_until_close({"close_ts": NOW + 48 * 3600}, NOW) - 48) < 0.01


def test_gate_unknown_clock_skips_time_checks():
    passes, reasons = followability_gate(0.52, 0.50, 5000.0, None)
    assert passes and reasons == []


# --- Nobel penny-market fix: dollar floor on volume spikes ------------------

def test_spike_dollar_floor_kills_penny_market_noise():
    # 10x baseline but only $8 of actual dollars traded
    assert detect_volume_spike(obs(rate=1000.0, dv_usd=8.0)) is None


def test_spike_fires_with_real_dollars():
    assert detect_volume_spike(obs(rate=1000.0, dv_usd=600.0)) is not None


# --- CZ/Swift fix: fresh-wallet exemption from the 90-day cap ---------------

def test_gate_max_days_blocks_normally():
    passes, reasons = followability_gate(0.52, 0.50, 5000.0, 120 * 24)
    assert not passes and any("too slow" in r for r in reasons)


def test_gate_fresh_wallet_exempt_from_max_days():
    passes, reasons = followability_gate(0.52, 0.50, 5000.0, 120 * 24,
                                         fresh_exempt=True)
    assert passes and reasons == []


def test_gate_fresh_exempt_does_not_skip_other_checks():
    passes, reasons = followability_gate(0.92, 0.91, 5000.0, 120 * 24,
                                         fresh_exempt=True)
    assert not passes and any("too late" in r for r in reasons)


# --- direction fix: copy the informed wallet, not the biggest print ----------

def test_side_follows_fresh_wallet_over_everything():
    signals = [
        {"type": "large_trade", "direction": -1},   # wrong-side NO whale
        {"type": "price_jump", "direction": -1},
        {"type": "fresh_wallet", "direction": 1},   # the insider
    ]
    assert choose_side(signals, price_drift=-0.1) == "yes"


def test_side_large_trade_beats_price_signals():
    signals = [{"type": "price_jump", "direction": -1},
               {"type": "large_trade", "direction": 1}]
    assert choose_side(signals, price_drift=-0.1) == "yes"


# --- archetype bypass ---------------------------------------------------------

def test_insider_archetype_detection():
    both = [{"type": "fresh_wallet", "points": 25},
            {"type": "large_trade", "points": 15}]
    assert is_insider_archetype(both)
    assert not is_insider_archetype(both[:1])
    assert not is_insider_archetype([{"type": "volume_spike", "points": 35}])


def test_archetype_score_sits_under_threshold_hence_the_bypass():
    # the documented misses scored 40-45; the bypass exists because of them
    assert 25 + 15 < CFG["ALERT_SCORE"]


# --- pseudonym epoch wallet age ------------------------------------------------

def test_wallet_age_from_default_name():
    created_ms = int((NOW - 3600) * 1000)
    age = wallet_age_from_name(f"0xeb4e5fc205fc65b731e8112d62c16dee7750cfd0-{created_ms}", NOW)
    assert age is not None and abs(age - 3600) < 1.0


def test_wallet_age_renamed_wallet_returns_none():
    assert wallet_age_from_name("drakedrakedrake", NOW) is None
    assert wallet_age_from_name("", NOW) is None
    assert wallet_age_from_name("0xabc-notanumber", NOW) is None


def test_wallet_age_rejects_future_timestamps():
    future_ms = int((NOW + 9999) * 1000)
    assert wallet_age_from_name(f"0xeb4e5fc205fc65b731e8112d62c16dee7750cfd0-{future_ms}", NOW) is None


# --- MONITOR-grade alerts --------------------------------------------------------

def monitor_alert(**overrides):
    base = {"title": "T", "platform": "poly", "market_id": "0xabc",
            "signals": ["fresh wallet loading up", "$5,000 single trade"],
            "side": "yes", "entry_price": 0.39, "category": "politics",
            "stake_usd": 0, "hours_to_close": 13.0, "score": 88, "url": "",
            "grade": "monitor", "gate_reasons": "resolves in 13h, no lag window"}
    base.update(overrides)
    return base


def test_monitor_alert_has_distinct_header_and_gate_line():
    msg = format_alert(monitor_alert())
    assert msg.splitlines()[0] == MONITOR_HEADER
    assert "🚧 Gated: resolves in 13h" in msg
    assert "informed side is YES" in msg
    assert "Window open" not in msg and "Suggested size" not in msg


def test_follow_alert_unchanged_by_default():
    msg = format_alert({**monitor_alert(), "grade": "follow",
                        "stake_usd": 50.0})
    assert msg.splitlines()[0].startswith("🚨🚨")
    assert "buy YES" in msg


def test_alert_window_unknown_when_clock_stale():
    msg = format_alert(monitor_alert(hours_to_close=None))
    assert "resolves in unknown" in msg

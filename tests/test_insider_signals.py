"""Research-backed signals added after the prior-art survey: price impact
per volume, repeat-actor wallet memory, within-trader bet size, and the
per-trigger CLV report."""

from tipoff import (
    CFG, compute_trigger_report, detect_price_impact, format_alert,
    observe_market, repeat_actor_signal, within_trader_signal,
)

NOW = 1_780_000_000.0


def impact_obs(dp=0.05, dv=50.0, base_impact=0.0002, n=20, dt_h=1.0):
    return {"dt_h": dt_h, "n": n, "dp": dp, "dv": dv,
            "impact": abs(dp) / dv if dv > 0 else None,
            "base_impact": base_impact, "rate": dv / dt_h,
            "base_mean": 100.0, "base_var": 100.0, "recent_moves": []}


# --- price impact per volume -------------------------------------------------

def test_impact_fires_on_outsized_move_per_volume():
    # 5c on 50 units = 0.001/unit vs baseline 0.0002 -> 5x
    sig = detect_price_impact(impact_obs())
    assert sig is not None
    assert sig["type"] == "price_impact" and sig["direction"] == 1
    assert "5x baseline" in sig["desc"]


def test_impact_silent_when_market_absorbs_volume_normally():
    assert detect_price_impact(impact_obs(base_impact=0.0009)) is None


def test_impact_needs_minimum_move():
    assert detect_price_impact(impact_obs(dp=0.02)) is None


def test_impact_phantom_guard():
    assert detect_price_impact(impact_obs(dv=5.0)) is None


def test_impact_needs_baseline_history():
    assert detect_price_impact(impact_obs(base_impact=0.0)) is None
    assert detect_price_impact(impact_obs(n=CFG["MIN_OBS"] - 1)) is None


def test_impact_baseline_accumulates_in_observe_market():
    m = {"platform": "kalshi", "id": "T", "title": "t", "category": "other",
         "vol": 0.0, "price": 0.50}
    entry, _ = observe_market(None, m, NOW)
    vol = 0.0
    for i in range(1, 10):
        vol += 100.0
        entry, obs = observe_market(
            entry, {**m, "vol": vol, "price": 0.50 + 0.001 * (i % 2)},
            NOW + i * 3600)
    assert entry.get("im", 0) > 0
    assert obs["base_impact"] > 0


# --- repeat actor -------------------------------------------------------------

def test_repeat_actor_fires_on_recent_reflag():
    rec = {"ts": NOW - 3 * 3600, "d": 1, "n": 1}
    sig = repeat_actor_signal(rec, 1, NOW)
    assert sig is not None and "2 flags" in sig["desc"]


def test_repeat_actor_notes_side_flip():
    rec = {"ts": NOW - 3600, "d": 1, "n": 2}
    sig = repeat_actor_signal(rec, -1, NOW)
    assert sig is not None and "flipped sides" in sig["desc"]


def test_repeat_actor_ignores_unknown_and_stale_wallets():
    assert repeat_actor_signal(None, 1, NOW) is None
    old = {"ts": NOW - (CFG["REPEAT_ACTOR_WINDOW_D"] + 1) * 86400, "d": 1}
    assert repeat_actor_signal(old, 1, NOW) is None


# --- within-trader bet size -----------------------------------------------------

def activity_trades(sizes):
    return [{"type": "TRADE", "usdcSize": s} for s in sizes]


def test_within_trader_fires_on_out_of_character_size():
    rows = activity_trades([100, 120, 90, 110, 100, 95])
    sig = within_trader_signal(rows, notional=1500.0)
    assert sig is not None
    assert "15x this wallet's typical" in sig["desc"]


def test_within_trader_silent_for_habitual_whale():
    # $15k trade from a wallet that always trades $10k: not out of character
    rows = activity_trades([10000] * 8)
    assert within_trader_signal(rows, notional=15000.0) is None


def test_within_trader_needs_history():
    rows = activity_trades([100, 100])
    assert within_trader_signal(rows, notional=5000.0) is None


def test_within_trader_ignores_non_trade_activity():
    rows = [{"type": "REWARD", "usdcSize": 2000}] * 10
    assert within_trader_signal(rows, notional=5000.0) is None


# --- per-trigger CLV report ------------------------------------------------------

def ledger_row(triggers, status="won", roi="0.5", clv="0.05"):
    return {"status": status, "triggers": triggers, "roi": roi, "clv": clv,
            "category": "politics"}


def test_trigger_report_groups_by_signal_type():
    rows = [
        ledger_row("price_jump+volume_spike"),
        ledger_row("price_jump", status="lost", roi="-1.0", clv="-0.03"),
        ledger_row("large_trade+fresh_wallet"),
        ledger_row("volume_spike", status="open", roi="", clv=""),  # ignored
    ]
    stats = compute_trigger_report(rows)
    assert stats["price_jump"]["graded"] == 2
    assert stats["volume_spike"]["graded"] == 1
    assert stats["fresh_wallet"]["graded"] == 1
    assert abs(stats["price_jump"]["avg_clv"] - 0.01) < 1e-9


def test_trigger_report_handles_legacy_rows_without_triggers():
    assert compute_trigger_report([ledger_row("")]) == {}


def test_alert_shows_signal_count():
    msg = format_alert({
        "title": "T", "platform": "kalshi", "market_id": "K",
        "signals": ["a", "b", "c"], "side": "yes", "entry_price": 0.5,
        "category": "politics", "stake_usd": 25.0, "hours_to_close": 30.0,
        "score": 70, "url": ""})
    assert "3 signals" in msg

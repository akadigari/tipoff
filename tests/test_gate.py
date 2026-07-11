"""Followability gate + scoring + sizing + calibration mode. The gate is the
whole point of the tool: a real signal you can't follow at a fair price is a
WATCH, not an alert."""

from tipoff import (
    CFG, calibration_status, choose_side, followability_gate, run_mode,
    score_signals, suggested_stake,
)


def gate(entry_price=0.52, signal_price=0.50, depth_usd=5000.0,
         hours_to_close=48.0, min_depth=None):
    return followability_gate(entry_price, signal_price, depth_usd,
                              hours_to_close, min_depth=min_depth)


def test_gate_passes_followable_setup():
    passes, reasons = gate()
    assert passes and reasons == []


def test_gate_rejects_price_already_moved():
    passes, reasons = gate(entry_price=0.92, signal_price=0.91)
    assert not passes
    assert any("too late" in r for r in reasons)


def test_gate_rejects_longshot_churn():
    passes, reasons = gate(entry_price=0.02, signal_price=0.02)
    assert not passes
    assert any("longshot" in r for r in reasons)


def test_gate_boundary_price_passes():
    passes, _ = gate(entry_price=CFG["GATE_MAX_PRICE"],
                     signal_price=CFG["GATE_MAX_PRICE"] - 0.01)
    assert passes


def test_gate_rejects_uncatchable_entry():
    # signal fired at 50c but the ask is 56c: fills won't resemble the signal
    passes, reasons = gate(entry_price=0.56, signal_price=0.50)
    assert not passes
    assert any("not catchable" in r for r in reasons)


def test_gate_catchable_boundary():
    passes, _ = gate(entry_price=0.50 + CFG["GATE_MAX_SLIP"],
                     signal_price=0.50)
    assert passes


def test_gate_rejects_thin_book():
    passes, reasons = gate(depth_usd=100.0)
    assert not passes
    assert any("thin" in r for r in reasons)


def test_gate_min_depth_override_polymarket_proxy():
    # $1500 passes the Kalshi floor but not the Polymarket liquidity proxy.
    passes, _ = gate(depth_usd=1500.0)
    assert passes
    passes, reasons = gate(depth_usd=1500.0,
                           min_depth=CFG["GATE_MIN_LIQUIDITY_USD"])
    assert not passes


def test_gate_rejects_fast_resolver_no_lag_window():
    # resolves in 12h: gate now requires >24h out
    passes, reasons = gate(hours_to_close=12.0)
    assert not passes
    assert any("no lag window" in r for r in reasons)


def test_gate_rejects_slow_resolver_dead_capital():
    passes, reasons = gate(hours_to_close=24 * 200)
    assert not passes
    assert any("too slow" in r for r in reasons)


def test_gate_collects_all_failures():
    passes, reasons = gate(entry_price=0.95, signal_price=0.85,
                           depth_usd=10.0, hours_to_close=1.0)
    assert not passes
    assert len(reasons) == 4  # too late, not catchable, thin, no lag window


# --- scoring -----------------------------------------------------------------

def test_score_sums_and_caps():
    sigs = [{"points": 35}, {"points": 35}, {"points": 30}, {"points": 25}]
    assert score_signals(sigs) == 100
    assert score_signals(sigs[:2]) == 70
    assert score_signals([]) == 0


def test_single_signal_cannot_alert_even_in_calibration():
    # Design invariant: no lone signal reaches even the loose calibration
    # threshold; alerts always require corroboration.
    max_single = {"volume_spike": 35, "price_jump": 35, "large_trade": 30,
                  "fresh_wallet": 25, "price_impact": 15, "chatter": 12,
                  "thin_market": 10, "cross_platform": 10,
                  "repeat_actor": 10, "within_trader": 8, "insiderable": 8}
    assert max(max_single.values()) < CFG["CALIB_ALERT_SCORE"]
    assert CFG["CALIB_ALERT_SCORE"] <= CFG["ALERT_SCORE"]


# --- side selection ------------------------------------------------------------

def test_choose_side_follows_directional_signals():
    assert choose_side([{"direction": 1}], price_drift=-0.5) == "yes"
    assert choose_side([{"direction": -1}], price_drift=0.5) == "no"


def test_choose_side_majority_of_directions():
    sigs = [{"direction": 1}, {"direction": 1}, {"direction": -1}]
    assert choose_side(sigs, price_drift=0.0) == "yes"


def test_choose_side_falls_back_to_drift():
    assert choose_side([{"type": "volume_spike"}], price_drift=0.03) == "yes"
    assert choose_side([{"type": "volume_spike"}], price_drift=-0.03) == "no"


# --- suggested stake -----------------------------------------------------------

def test_stake_scales_with_score():
    assert suggested_stake(60, depth_usd=100000) == CFG["PAPER_STAKE_BASE"]
    assert suggested_stake(80, depth_usd=100000) == CFG["PAPER_STAKE_BASE"] * 2
    assert suggested_stake(95, depth_usd=100000) == CFG["PAPER_STAKE_BASE"] * 4


def test_stake_capped_by_depth():
    # never suggest more than 10% of visible size
    assert suggested_stake(95, depth_usd=600.0) <= 60.0


def test_stake_has_floor():
    assert suggested_stake(60, depth_usd=50.0) >= 10.0


# --- calibration week ------------------------------------------------------------

DAY = 86400.0
T0 = 1_780_000_000.0


def test_calibration_active_first_week():
    active, day = calibration_status(T0, T0 + 2.5 * DAY)
    assert active and day == 3
    assert run_mode(active) == "calib"


def test_calibration_ends_after_calib_days():
    active, day = calibration_status(T0, T0 + CFG["CALIB_DAYS"] * DAY + 1)
    assert not active
    assert run_mode(active) == "normal"


def test_calibration_first_run_is_day_one():
    active, day = calibration_status(T0, T0)
    assert active and day == 1

"""Coordination detector — N distinct wallets buying the same side within a
tight window. The documented insider signature (Iran Feb 2026: 8 wallets,
same 2 seconds) that no per-wallet threshold can see."""

from tipoff import CFG, choose_side, detect_coordination

NOW = 1_780_000_000.0


def trade(wallet, t_offset, side="BUY", idx=0, size=2000, price=0.50):
    return {"proxyWallet": wallet, "timestamp": NOW + t_offset, "side": side,
            "outcomeIndex": idx, "size": size, "price": price}


def test_fires_on_three_wallets_same_second_same_side():
    trades = [trade("0xa", 0), trade("0xb", 1), trade("0xc", 2)]
    sig = detect_coordination(trades, since_ts=NOW - 10)
    assert sig is not None
    assert sig["type"] == "coordination" and sig["direction"] == 1
    assert "3 wallets bought YES" in sig["desc"]


def test_reports_the_largest_cluster():
    trades = [trade(f"0x{i}", i * 0.5) for i in range(6)]  # 6 within 3s
    sig = detect_coordination(trades, since_ts=NOW - 10)
    assert sig is not None and "6 wallets" in sig["desc"]
    assert sig["points"] == 20  # capped


def test_same_wallet_repeated_is_not_coordination():
    # one wallet firing three times is not three colluders
    trades = [trade("0xa", 0), trade("0xa", 1), trade("0xa", 2)]
    assert detect_coordination(trades, since_ts=NOW - 10) is None


def test_spread_out_trades_do_not_coordinate():
    # three wallets but minutes apart — not a coordinated burst
    trades = [trade("0xa", 0), trade("0xb", 120), trade("0xc", 300)]
    assert detect_coordination(trades, since_ts=NOW - 1000) is None


def test_opposite_sides_do_not_coordinate():
    # two YES + one NO in the same window: no 3-wallet same-side cluster
    trades = [trade("0xa", 0), trade("0xb", 1),
              trade("0xc", 2, side="SELL")]  # sell of YES leg = toward NO
    assert detect_coordination(trades, since_ts=NOW - 10) is None


def test_sell_of_no_leg_counts_toward_yes():
    # buying YES, buying YES, and SELLING the No leg all push YES
    trades = [trade("0xa", 0), trade("0xb", 1),
              trade("0xc", 2, side="SELL", idx=1)]
    sig = detect_coordination(trades, since_ts=NOW - 10)
    assert sig is not None and sig["direction"] == 1


def test_dust_trades_excluded_from_cluster():
    trades = [trade("0xa", 0, size=10, price=0.5),   # $5, dust
              trade("0xb", 1, size=10, price=0.5),
              trade("0xc", 2, size=10, price=0.5)]
    assert detect_coordination(trades, since_ts=NOW - 10) is None


def test_ignores_trades_before_since():
    trades = [trade("0xa", -100), trade("0xb", -99), trade("0xc", -98)]
    assert detect_coordination(trades, since_ts=NOW - 10) is None


def test_needs_min_wallets():
    trades = [trade("0xa", 0), trade("0xb", 1)]  # only 2
    assert detect_coordination(trades, since_ts=NOW - 10) is None


def test_two_clusters_far_apart_still_detected():
    # a NO cluster early, a bigger YES cluster later — report the bigger
    trades = [trade("0xa", 0, side="SELL"), trade("0xb", 1, side="SELL"),
              trade("0xc", 2, side="SELL"),
              trade("0xd", 500), trade("0xe", 501),
              trade("0xf", 502), trade("0xg", 503)]
    sig = detect_coordination(trades, since_ts=NOW - 10)
    assert sig is not None
    assert sig["direction"] == 1 and "4 wallets" in sig["desc"]


# --- integration with side selection ------------------------------------------

def test_choose_side_prioritizes_coordination():
    # coordination points YES; a lone large trade points NO — follow the crowd
    signals = [{"type": "large_trade", "direction": -1},
               {"type": "coordination", "direction": 1}]
    assert choose_side(signals, price_drift=-0.1) == "yes"


def test_coordination_stays_corroborator_only():
    # max coordination score must not clear even the loose calib threshold
    assert min(20, 5 + 4 * 3) < CFG["CALIB_ALERT_SCORE"]

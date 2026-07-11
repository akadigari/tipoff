"""Signal detection: volume spike, price jump, large trade, fresh wallet,
category tagging. All pure functions, no network."""

import tipoff
from tipoff import (
    CFG, categorize, detect_large_trades, detect_price_jump,
    detect_volume_spike, is_fresh_wallet, observe_market,
)

NOW = 1_780_000_000.0


def make_obs(rate=100.0, base_mean=100.0, base_var=100.0, n=20,
             dp=0.0, dt_h=1.0, recent_moves=None):
    return {
        "dt_h": dt_h, "rate": rate, "dp": dp,
        "base_mean": base_mean, "base_var": base_var, "n": n,
        "recent_moves": recent_moves if recent_moves is not None
        else [0.01] * 8,
    }


# --- volume spike ---------------------------------------------------------

def test_volume_spike_fires_on_10x_baseline():
    obs = make_obs(rate=1000.0, base_mean=100.0, base_var=100.0)
    sig = detect_volume_spike(obs)
    assert sig is not None
    assert sig["type"] == "volume_spike"
    assert sig["points"] >= 25


def test_volume_spike_silent_on_normal_volume():
    assert detect_volume_spike(make_obs(rate=120.0)) is None


def test_volume_spike_needs_warmup_history():
    obs = make_obs(rate=5000.0, n=CFG["MIN_OBS"] - 1)
    assert detect_volume_spike(obs) is None


def test_volume_spike_ignores_dust_markets():
    # 50x baseline but only 100 contracts of absolute delta: noise.
    obs = make_obs(rate=100.0, base_mean=2.0, base_var=1.0)
    assert detect_volume_spike(obs) is None


def test_volume_spike_skips_stale_gap():
    obs = make_obs(rate=1000.0, dt_h=CFG["MAX_GAP_HOURS"] + 1)
    assert detect_volume_spike(obs) is None


def test_volume_spike_skips_first_observation():
    assert detect_volume_spike({"dt_h": None}) is None


# --- price jump ------------------------------------------------------------

def test_price_jump_fires_on_big_move():
    sig = detect_price_jump(make_obs(dp=0.12), hours_to_close=100.0)
    assert sig is not None
    assert sig["direction"] == 1
    assert "+12c" in sig["desc"]


def test_price_jump_downward_direction():
    sig = detect_price_jump(make_obs(dp=-0.10), hours_to_close=100.0)
    assert sig is not None and sig["direction"] == -1


def test_price_jump_silent_on_small_move():
    assert detect_price_jump(make_obs(dp=0.03), hours_to_close=100.0) is None


def test_price_jump_scheduled_news_proxy():
    # Same jump, but the market resolves in 2h: presumed event-driven.
    assert detect_price_jump(make_obs(dp=0.12), hours_to_close=2.0) is None


def test_price_jump_respects_market_chop():
    # 9c move in a market that routinely moves 5c is not a jump.
    obs = make_obs(dp=0.09, recent_moves=[0.05] * 8)
    assert detect_price_jump(obs, hours_to_close=100.0) is None


def test_price_jump_skips_stale_gap():
    obs = make_obs(dp=0.20, dt_h=CFG["PRICE_JUMP_MAX_AGE_H"] + 1)
    assert detect_price_jump(obs, hours_to_close=100.0) is None


# --- large trade (on-chain) -------------------------------------------------

def trade(size, price, side="BUY", idx=0, ts=NOW, wallet="0xabc"):
    return {"size": size, "price": price, "side": side, "outcomeIndex": idx,
            "timestamp": ts, "proxyWallet": wallet}


def test_large_trade_fires_and_reports_notional():
    sig = detect_large_trades([trade(20000, 0.50)], since_ts=NOW - 3600)
    assert sig is not None
    assert sig["notional"] == 10000
    assert sig["direction"] == 1  # bought YES


def test_large_trade_sell_of_yes_is_bearish():
    sig = detect_large_trades([trade(20000, 0.50, side="SELL")],
                              since_ts=NOW - 3600)
    assert sig is not None and sig["direction"] == -1


def test_large_trade_buy_of_no_is_bearish():
    sig = detect_large_trades([trade(20000, 0.50, idx=1)], since_ts=NOW - 3600)
    assert sig is not None and sig["direction"] == -1


def test_large_trade_ignores_old_trades():
    old = trade(20000, 0.50, ts=NOW - 7200)
    assert detect_large_trades([old], since_ts=NOW - 3600) is None


def test_large_trade_ignores_small_trades():
    assert detect_large_trades([trade(100, 0.50)], since_ts=NOW - 3600) is None


def test_large_trade_picks_biggest():
    trades = [trade(12000, 0.50), trade(40000, 0.50), trade(11000, 0.50)]
    sig = detect_large_trades(trades, since_ts=NOW - 3600)
    assert sig["notional"] == 20000


# --- fresh wallet ------------------------------------------------------------

def activity(age_days):
    return {"timestamp": NOW - age_days * 86400}


def test_fresh_wallet_young_short_history():
    rows = [activity(1), activity(2)]
    assert is_fresh_wallet(rows, fetch_limit=50, ts=NOW)


def test_fresh_wallet_old_account_rejected():
    rows = [activity(1), activity(100)]
    assert not is_fresh_wallet(rows, fetch_limit=50, ts=NOW)


def test_fresh_wallet_full_page_means_veteran():
    # 50 rows back from a limit-50 fetch: history is truncated, assume old.
    rows = [activity(1)] * 50
    assert not is_fresh_wallet(rows, fetch_limit=50, ts=NOW)


def test_fresh_wallet_empty_history_rejected():
    assert not is_fresh_wallet([], fetch_limit=50, ts=NOW)


# --- baseline bookkeeping (observe_market) ----------------------------------

def market(vol=1000.0, price=0.50):
    return {"platform": "kalshi", "id": "T", "title": "t", "category": "other",
            "vol": vol, "price": price}


def test_observe_market_first_sighting_no_obs():
    entry, obs = observe_market(None, market(), NOW)
    assert obs["dt_h"] is None
    assert entry["n"] == 0 and entry["v"] == 1000.0


def test_observe_market_computes_rate_and_move():
    entry, _ = observe_market(None, market(), NOW)
    entry, obs = observe_market(entry, market(vol=1500.0, price=0.60),
                                NOW + 3600)
    assert abs(obs["rate"] - 500.0) < 1e-6
    assert abs(obs["dp"] - 0.10) < 1e-9
    assert entry["n"] == 1


def test_observe_market_baseline_stats_are_pre_update():
    entry, _ = observe_market(None, market(), NOW)
    for i in range(1, 11):
        entry, obs = observe_market(
            entry, market(vol=1000.0 + i * 100), NOW + i * 3600)
    # baseline mean handed to detectors reflects history, not the new point
    assert obs["base_mean"] > 0
    assert obs["n"] == 9


def test_observe_market_move_window_capped():
    entry, _ = observe_market(None, market(), NOW)
    for i in range(1, 30):
        entry, _ = observe_market(
            entry, market(vol=1000.0 + i, price=0.50 + (i % 2) * 0.01),
            NOW + i * 3600)
    assert len(entry["mv"]) <= CFG["MAX_MOVE_WINDOW"]


# --- category tagging --------------------------------------------------------

def test_categorize_crypto_beats_platform_category():
    assert categorize("Bitcoin above $150k on Friday?", "Financials") == "crypto"


def test_categorize_uses_kalshi_category():
    assert categorize("Some obscure race", "Elections") == "politics"
    assert categorize("Random award thing", "Entertainment") == "entertainment"


def test_categorize_keywords_fallback():
    assert categorize("Will the Chiefs win the Super Bowl?") == "sports"
    assert categorize("Who wins Best Picture at the Oscars?") == "entertainment"
    assert categorize("Will the ceasefire hold through August?") == "politics"


def test_categorize_other_when_unknown():
    assert categorize("Will it rain in Miami tomorrow?") == "other"

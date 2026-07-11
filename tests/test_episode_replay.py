"""End-to-end replay of REAL documented insider episodes through the actual
shipped code path (observe_market -> detectors -> scoring -> gate), not a
simulation. Each fixture is the true hourly price/volume series pulled from
Polymarket for a market where insider trading was publicly documented.

The question these answer: "would the deployed bot have flagged this?"
"""

import json
from pathlib import Path

from tipoff import (
    CFG, detect_price_impact, detect_price_jump, detect_volume_spike,
    hours_until_close, is_insider_archetype, observe_market, score_signals,
)

FIXTURES = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIXTURES / f"{name}.json").read_text())


def replay(series, close_ts, platform="poly"):
    """Feed a real hourly series through production observe_market exactly as
    a live run would, returning per-hour (market, obs, signals). This is the
    real code path — same baseline math, same detectors."""
    entry = None
    out = []
    for bar in series:
        m = {"platform": platform, "id": "EP", "title": "episode",
             "category": "politics", "vol": bar["vol"], "price": bar["price"],
             "close_ts": close_ts}
        entry, obs = observe_market(entry, m, bar["ts"])
        htc = hours_until_close({"close_ts": close_ts}, bar["ts"])
        signals = []
        for det in (detect_volume_spike(obs),
                    detect_price_jump(obs, htc),
                    detect_price_impact(obs)):
            if det:
                signals.append(det)
        out.append({"bar": bar, "obs": obs, "signals": signals,
                    "score": score_signals(signals)})
    return out


# --- Nobel Peace Prize 2025 leak (Maria Corina Machado) ---------------------
# Real Polymarket series: YES sat at ~1.7% for days, then at the anomaly hour
# (2025-10-09 22:00 UTC, ~11h before the announcement) jumped 3.7c -> 39c on
# $32k volume. The Nobel Institute later confirmed a systems breach.

def test_nobel_bot_flags_the_leak_hour():
    series = load("nobel_2025_machado")
    # scheduled close was ~1-13h out during the anomaly (near resolution) —
    # the exact condition that silently gated this to death before the fix
    close_ts = series[-1]["ts"]
    result = replay(series, close_ts)

    # the anomaly hour is the first time price crosses 0.30
    leak_i = next(i for i, r in enumerate(result) if r["bar"]["price"] > 0.30)
    leak = result[leak_i]

    # the bot MUST produce signals here — this is the whole point
    assert leak["signals"], "bot saw nothing on the documented Nobel leak hour"
    fired = {s["type"] for s in leak["signals"]}
    # a 10x longshot repricing on huge volume is spike + jump
    assert "volume_spike" in fired
    assert "price_jump" in fired, "extreme repricing must survive the " \
        "scheduled-news proxy (this is the fix the backtest forced)"
    assert leak["score"] >= CFG["ALERT_SCORE"], \
        f"leak hour scored {leak['score']}, below alert threshold"


def test_nobel_quiet_days_stay_silent():
    # the 1.7% plateau before the leak must NOT fire — no false positives on
    # the boring hours, or the signal means nothing
    series = load("nobel_2025_machado")
    result = replay(series, series[-1]["ts"])
    leak_i = next(i for i, r in enumerate(result) if r["bar"]["price"] > 0.30)
    pre_leak = result[:leak_i]
    # allow warm-up; check the settled quiet hours produced no alert-level score
    quiet = [r for r in pre_leak if r["obs"].get("n", 0) >= CFG["MIN_OBS"]]
    assert quiet, "fixture should include warmed-up quiet hours"
    assert all(r["score"] < CFG["ALERT_SCORE"] for r in quiet), \
        "bot cried insider on a boring 1.7% plateau hour"


def test_nobel_extreme_jump_beats_scheduled_news_proxy():
    # Direct proof of the fix. In the real episode the gamma endDate was ~12h
    # earlier than the true close, which pulled the leak hour INSIDE the 12h
    # scheduled-news window and silently suppressed the price_jump. Reproduce
    # that exact broken clock and assert the jump now survives because the
    # repricing (3.7c -> 39c) is extreme.
    series = load("nobel_2025_machado")
    leak_bar = next(b for b in series if b["price"] > 0.30)
    stale_close = leak_bar["ts"] + 2 * 3600  # leak now 2h before "close"
    result = replay(series, stale_close)
    leak = next(r for r in result if r["bar"]["price"] > 0.30)
    htc = hours_until_close({"close_ts": stale_close}, leak["bar"]["ts"])
    assert htc is not None and htc < CFG["SCHEDULED_NEWS_MIN_H"], \
        "precondition: leak sits inside the news window under the stale clock"
    assert any(s["type"] == "price_jump" for s in leak["signals"]), \
        "extreme repricing was wrongly suppressed as scheduled news"


# --- Operation Rising Lion (June 2025, criminal indictment) -----------------
# Real series for "Israel military action against Iran before July". An IAF
# reservist leaked the strike date; the strike (~June 13) resolved the market.

def test_rising_lion_bot_reacts_to_the_strike_repricing():
    series = load("rising_lion_2025")
    close_ts = series[-1]["ts"] + 6 * 3600
    result = replay(series, close_ts)
    # final bar is the strike repricing (0.57 -> 0.915)
    move_bars = [r for r in result if r["signals"]]
    assert move_bars, "bot saw nothing across the entire strike window"
    # the big repricing hour must carry a price signal
    jump_hours = [r for r in result if any(
        s["type"] in ("price_jump", "price_impact") for s in r["signals"])]
    assert jump_hours, "no price signal on a market that moved 0.57 -> 0.92"


# --- guardrail: the shipped archetype rule catches the score-40 misses ------

def test_archetype_catches_documented_subthreshold_insiders():
    # bigwinner01 (40), Mikeymike53 (41), romanticpaul (45) all scored under
    # the 55 bar in the backtest; the archetype rule is what saves them.
    # Verify the shipped predicate flags exactly that fresh+large shape.
    documented_shape = [
        {"type": "fresh_wallet", "points": 25, "direction": 1},
        {"type": "large_trade", "points": 16, "direction": 1},
    ]
    assert score_signals(documented_shape) < CFG["ALERT_SCORE"]
    assert is_insider_archetype(documented_shape), \
        "shipped archetype rule fails to flag the documented insider shape"

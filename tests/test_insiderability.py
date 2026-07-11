"""Insiderability taxonomy — derived from the documented episode history:
every verified insider case resolved on a private human decision; none
happened in a game outcome (nobody knows a live game's result in advance).
"""

from tipoff import CFG, insiderability, scan_market

NOW = 1_780_000_000.0


# --- game outcomes: no insider can exist -------------------------------------

def test_game_outcome_markets_are_none():
    cases = [
        ("Norway vs England: both teams to score in 1st half?", "sports"),
        ("Lakers vs Celtics moneyline", "sports"),
        ("Will Spain win on 2026-07-10?", "sports"),
        ("Chiefs total points over/under 27.5", "sports"),
        ("Faker to win map 2?", "sports"),
    ]
    for title, cat in cases:
        assert insiderability(title, cat) == "none", title


def test_generic_sports_without_game_pattern_stays_scannable():
    # a season-long future isn't a live game; leave it normal
    assert insiderability("Will the Jets make the playoffs?",
                          "sports") == "normal"


def test_sports_decision_markets_stay_hot():
    # injuries, retirements, trades, awards DO leak — these are decisions
    cases = [
        "Will Patrick Mahomes retire before the 2027 season?",
        "Will LeBron be traded to the Warriors?",
        "Will Caitlin Clark be suspended for game 3?",
    ]
    for title in cases:
        assert insiderability(title, "sports") == "high", title


# --- decision markets: where every documented episode happened ----------------

def test_documented_episode_shapes_are_high():
    cases = [
        ("Will Maria Corina Machado win the Nobel Peace Prize?", "politics"),
        ("Will Trump pardon Changpeng Zhao in 2025?", "politics"),
        ("Taylor Swift and Travis Kelce engaged in 2025?", "entertainment"),
        ("Andy Byron out as Astronomer CEO by Friday?", "other"),
        ("US military action against Iran before July?", "politics"),
        ("Will George Santos attend the State of the Union?", "politics"),
    ]
    for title, cat in cases:
        assert insiderability(title, cat) == "high", title


def test_plain_markets_are_normal():
    assert insiderability("Will it rain in Miami tomorrow?", "other") == "normal"
    assert insiderability("Bitcoin above $150k on Friday?", "crypto") == "normal"


# --- scan integration ----------------------------------------------------------

def make_market(title, category, vol=100000.0, price=0.50):
    return {"platform": "kalshi", "id": "T1", "title": title,
            "category": category, "vol": vol, "price": price,
            "close_ts": NOW + 100 * 3600, "vol24": 50000.0,
            "yes_ask": price + 0.01, "no_ask": 1 - price + 0.01,
            "depth_yes_usd": 5000.0, "depth_no_usd": 5000.0, "url": ""}


def warm_entry(m, runs=12):
    entry = None
    budget = {"trades": 99, "wallets": 99, "comments": 99}  # exhausted
    for i in range(runs):
        mm = dict(m, vol=m["vol"] + i * 500)
        entry, _, _ = scan_market(mm, entry, NOW + i * 3600, budget, {})
    return entry, budget


def test_scan_skips_signals_on_game_markets():
    m = make_market("Norway vs England: both teams to score?", "sports")
    entry, budget = warm_entry(m)
    # massive spike + jump on a game market: still zero signals
    hot = dict(m, vol=m["vol"] + 500000, price=0.70)
    _, signals, _ = scan_market(hot, entry, NOW + 13 * 3600, budget, {})
    assert signals == []


def test_scan_boosts_decision_markets():
    m = make_market("Will the CEO resign by Friday?", "politics")
    entry, budget = warm_entry(m)
    hot = dict(m, vol=m["vol"] + 500000, price=0.70)
    _, signals, _ = scan_market(hot, entry, NOW + 13 * 3600, budget, {})
    types = {s["type"] for s in signals}
    assert "volume_spike" in types and "price_jump" in types
    assert "insiderable" in types
    boost = next(s for s in signals if s["type"] == "insiderable")
    assert boost["points"] == CFG["INSIDERABLE_POINTS"]


def test_insiderable_is_corroborator_only():
    # a quiet decision market produces no signals, so no lone boost
    m = make_market("Will the CEO resign by Friday?", "politics")
    entry, budget = warm_entry(m)
    calm = dict(m, vol=m["vol"] + 500, price=0.50)
    _, signals, _ = scan_market(calm, entry, NOW + 13 * 3600, budget, {})
    assert signals == []

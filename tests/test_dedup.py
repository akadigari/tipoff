"""Cross-platform confirmation + one-alert-per-story dedup."""

from tipoff import (
    cross_platform_confirm, dedup_alerts, title_similarity, title_tokens,
)


def cand(platform="kalshi", event="EV1", market_id="M1", score=60,
         title="Will the Fed cut rates in September?", signals=None):
    return {"platform": platform, "event": event, "market_id": market_id,
            "id": market_id, "score": score, "title": title,
            "signals": signals if signals is not None else
            [{"type": "price_jump", "desc": "jump", "points": 30}]}


# --- title matching ------------------------------------------------------------

def test_title_tokens_strips_stopwords():
    toks = title_tokens("Will the Fed cut rates in September?")
    assert "will" not in toks and "the" not in toks
    assert {"fed", "cut", "rates", "september"} <= toks


def test_similarity_high_for_same_story():
    a = "Will the Fed cut rates in September?"
    b = "Fed cuts rates at the September meeting?"
    assert title_similarity(a, b) >= 0.5


def test_similarity_number_veto_different_strikes():
    # same family, different strikes — must NOT be treated as one story
    a = "Will Bitcoin hit $150000 by December 31?"
    b = "Will Bitcoin hit $200000 by December 31?"
    assert title_similarity(a, b) == 0.0


def test_similarity_zero_for_unrelated():
    assert title_similarity("Will the Fed cut rates?",
                            "Who wins Best Picture at the Oscars?") < 0.2


# --- cross-platform confirmation --------------------------------------------------

def test_cross_platform_confirm_boosts_both_twins():
    a = cand(platform="kalshi", title="Will the Fed cut rates in September?")
    b = cand(platform="poly", event="fed-sept",
             title="Fed cuts rates at the September meeting?")
    cross_platform_confirm([a, b])
    assert any(s["type"] == "cross_platform" for s in a["signals"])
    assert any(s["type"] == "cross_platform" for s in b["signals"])
    assert "confirmed on poly" in a["signals"][-1]["desc"]


def test_cross_platform_no_boost_same_platform():
    a = cand(market_id="M1")
    b = cand(market_id="M2")  # same platform, same title
    cross_platform_confirm([a, b])
    assert not any(s["type"] == "cross_platform" for s in a["signals"])


def test_cross_platform_no_boost_unrelated_titles():
    a = cand(platform="kalshi")
    b = cand(platform="poly", title="Who wins Best Picture at the Oscars?")
    cross_platform_confirm([a, b])
    assert not any(s["type"] == "cross_platform" for s in a["signals"])


def test_cross_platform_confirm_added_once():
    a = cand(platform="kalshi", title="Will the Fed cut rates in September?")
    b = cand(platform="poly", title="Fed cut rates September?")
    c = cand(platform="poly", market_id="M3", event="EV3",
             title="Fed cutting rates in September meeting?")
    cross_platform_confirm([a, b, c])
    assert sum(s["type"] == "cross_platform" for s in a["signals"]) == 1


# --- alert dedup -------------------------------------------------------------------

def test_dedup_keeps_top_scorer_per_event():
    # six legs of one event all spiking on the same news
    legs = [cand(market_id=f"M{i}", score=50 + i) for i in range(3)]
    kept, dropped = dedup_alerts(legs)
    assert len(kept) == 1
    assert kept[0]["score"] == 52
    assert len(dropped) == 2
    assert all("duplicate leg" in reason for _, reason in dropped)


def test_dedup_drops_cross_platform_twin():
    a = cand(platform="kalshi", score=70,
             title="Will the Fed cut rates in September?")
    b = cand(platform="poly", event="fed-sept", market_id="0xabc", score=60,
             title="Fed cuts rates at the September meeting?")
    kept, dropped = dedup_alerts([a, b])
    assert len(kept) == 1 and kept[0]["platform"] == "kalshi"
    assert "same story alerted on kalshi" in dropped[0][1]


def test_dedup_keeps_distinct_stories():
    a = cand(event="EV1", title="Will the Fed cut rates?")
    b = cand(event="EV2", market_id="M2",
             title="Who wins Best Picture at the Oscars?")
    kept, dropped = dedup_alerts([a, b])
    assert len(kept) == 2 and not dropped

"""Insiderability taxonomy: derived from the documented episode history,
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


def test_play_determined_futures_are_none_too():
    # tournaments, scorer races, playoff runs: decided on the field,
    # zero documented insider episodes in any play-determined outcome
    cases = [
        ("Will Harry Kane be the top goal scorer at the 2026 FIFA"
         " World Cup?", "sports"),
        ("Will Norway reach the Semifinals at the 2026 FIFA World Cup?",
         "sports"),
        ("Will the Jets make the playoffs?", "sports"),
        ("Golden Boot Winner: Erling Haaland", "sports"),
    ]
    for title, cat in cases:
        assert insiderability(title, cat) == "none", title


def test_esports_flows_to_none_via_categorize():
    # esports reach "none" through the real pipeline: categorize() now
    # recognizes esports titles as sports, and sports outcomes are "none"
    from tipoff import categorize
    title = "Will Hanwha Life Esports win MSI 2026?"
    cat = categorize(title)
    assert cat == "sports"
    assert insiderability(title, cat) == "none"


def test_sports_decision_markets_stay_hot():
    # injuries, retirements, trades, awards DO leak, these are decisions
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


# --- news check ("no public explanation" verification) -------------------------

from tipoff import apply_news_check, count_recent_news, news_query  # noqa: E402
import tipoff  # noqa: E402


def rss(pub_dates):
    items = "".join(f"<item><title>x</title><pubDate>{d}</pubDate></item>"
                    for d in pub_dates)
    return f'<rss version="2.0"><channel>{items}</channel></rss>'


def test_news_query_strips_stopwords_and_years():
    q = news_query("Will Trump pardon Changpeng Zhao in 2025?")
    assert q == "Trump pardon Changpeng Zhao"


def test_count_recent_news_windows_correctly():
    text = rss(["Fri, 11 Jul 2026 02:00:00 GMT",   # inside 24h of NOW-ish
                "Tue, 01 Jul 2025 00:00:00 GMT"])  # ancient
    ts = 1783742400.0  # 2026-07-11 04:00 UTC
    assert count_recent_news(text, ts, 24.0) == 1


def test_count_recent_news_bad_xml_is_zero():
    assert count_recent_news("not xml at all", NOW, 24.0) == 0


def test_apply_news_check_marks_unexplained_and_explained(monkeypatch):
    counts = {"quiet market move": 0, "loud market move": 5}
    monkeypatch.setattr(tipoff, "fetch_news_count",
                        lambda q, ts: counts.get(q))
    quiet = {"title": "quiet market move", "signals": []}
    loud = {"title": "loud market move", "signals": []}
    broken = {"title": "", "signals": []}  # fetch returns None
    apply_news_check([quiet, loud, broken], NOW)
    assert any(s["type"] == "no_public_news" for s in quiet["signals"])
    assert "news_note" not in quiet
    assert loud["signals"] == [] and "likely reacting" in loud["news_note"]
    assert broken["signals"] == [] and "news_note" not in broken


def test_apply_news_check_respects_budget(monkeypatch):
    calls = []
    monkeypatch.setattr(tipoff, "fetch_news_count",
                        lambda q, ts: calls.append(q) or 0)
    cands = [{"title": f"market {i}", "signals": []} for i in range(20)]
    apply_news_check(cands, NOW)
    assert len(calls) == tipoff.CFG["MAX_NEWS_CHECKS"]


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

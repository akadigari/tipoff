"""Wallet roster grading: the wallet-first pivot, graded against our own
research log with a sample gate and a luck test."""

import roster
from roster import (
    FOLLOW_EDGE, KNOWN_INSIDERS, MIN_TRADES, binomial_luck_p, build_roster,
    grade_wallets, wallet_verdict,
)


def row(wallet, side="yes", yes_price="0.50", p_24h="0.55", market_id="M1"):
    return {"wallet": wallet, "side": side, "yes_price": yes_price,
            "p_24h": p_24h, "p_1h": p_24h, "p_6h": p_24h,
            "market_id": market_id}


# --- luck test ---------------------------------------------------------------

def test_coin_flip_is_not_significant():
    # 6 of 12 the wallet's way is exactly chance
    assert binomial_luck_p(6, 12) > 0.4


def test_strong_run_beats_luck():
    # 18 of 20 the wallet's way is very unlikely by chance
    assert binomial_luck_p(18, 20) < 0.01


def test_no_moves_is_no_evidence():
    assert binomial_luck_p(0, 0) == 1.0


def test_luck_p_rewards_larger_samples():
    # same 75% hit rate, but more samples is more convincing
    assert binomial_luck_p(30, 40) < binomial_luck_p(3, 4)


# --- verdicts ----------------------------------------------------------------

def test_thin_wallets_get_no_verdict():
    assert wallet_verdict(MIN_TRADES - 1, 0.99, 0.0001) == "INSUFFICIENT DATA"


def test_watch_needs_edge_and_luck():
    assert wallet_verdict(50, 0.05, 0.01).startswith("WATCH")


def test_edge_without_beating_luck_is_only_promising():
    assert wallet_verdict(50, 0.05, 0.30).startswith("PROMISING")


def test_negative_average_is_fade():
    assert wallet_verdict(50, -0.05, 0.01).startswith("FADE")


def test_flat_edge_is_noise():
    assert wallet_verdict(50, 0.0, 0.01).startswith("NOISE")


# --- grading -----------------------------------------------------------------

def test_grades_a_consistent_wallet_as_watch():
    # a wallet whose flagged trades always ran +5c, across many samples
    rows = [row("0xsharp", market_id=f"M{i}") for i in range(MIN_TRADES + 3)]
    graded = {g["wallet"]: g for g in grade_wallets(rows, {})}
    g = graded["0xsharp"]
    assert g["n"] == MIN_TRADES + 3
    assert g["hit_rate"] == 1.0 and g["avg"] > 0
    assert g["verdict"].startswith("WATCH")


def test_grades_a_fader_correctly():
    # every flagged trade moved 5c AGAINST the wallet's side
    rows = [row("0xfade", p_24h="0.45", market_id=f"M{i}")
            for i in range(MIN_TRADES + 1)]
    g = {x["wallet"]: x for x in grade_wallets(rows, {})}["0xfade"]
    assert g["avg"] < 0 and g["verdict"].startswith("FADE")


def test_wallet_with_no_forward_data_is_insufficient():
    rows = [row("0xnew", p_24h="")]  # flagged but no filled horizon yet
    g = {x["wallet"]: x for x in grade_wallets(rows, {})}["0xnew"]
    assert g["n"] == 0 and g["markets"] == 1
    assert g["verdict"] == "INSUFFICIENT DATA"


def test_distinct_market_count_and_flags_join():
    rows = [row("0xa", market_id="M1"), row("0xa", market_id="M2"),
            row("0xa", market_id="M2")]
    state = {"0xa": {"flags": 9, "dir": 1}}
    g = {x["wallet"]: x for x in grade_wallets(rows, state)}["0xa"]
    assert g["markets"] == 2 and g["flags"] == 9


def test_rows_without_wallet_are_ignored():
    rows = [row(""), {"side": "yes", "yes_price": "0.5", "p_24h": "0.6"}]
    assert grade_wallets(rows, {}) == []


def test_no_side_direction_is_respected():
    # picked NO at 0.50, price fell to 0.45: that is +5c the wallet's way
    rows = [row("0xno", side="no", p_24h="0.45", market_id=f"M{i}")
            for i in range(MIN_TRADES + 1)]
    g = {x["wallet"]: x for x in grade_wallets(rows, {})}["0xno"]
    assert g["avg"] > 0


# --- report ------------------------------------------------------------------

def test_roster_report_sections_and_caveat():
    rows = [row("0xsharp", market_id=f"M{i}") for i in range(MIN_TRADES + 5)]
    text = build_roster(grade_wallets(rows, {}), "2026-07-19T00:00:00Z")
    assert "# Wallet roster" in text
    assert "Watch list" in text and "Documented known insiders" in text
    # the selection-bias caveat must be present, this is the honest part
    assert "market makers" in text and "not quiet insiders" in text
    assert "0xsharp" in text


def test_known_insiders_listed_in_report():
    text = build_roster([], "2026-07-19T00:00:00Z")
    assert "romanticpaul" in text and "bigwinner01" in text
    assert len(KNOWN_INSIDERS) >= 5


def test_main_handles_no_data(monkeypatch, capsys):
    monkeypatch.setattr(roster, "load_rows", lambda *a, **k: [])
    assert roster.main() == 0
    assert "nothing to grade" in capsys.readouterr().out


def test_main_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(roster, "ROSTER_FILE", tmp_path / "ROSTER.md")
    monkeypatch.setattr(roster, "load_rows",
                        lambda *a, **k: [row("0xa", market_id=f"M{i}")
                                         for i in range(MIN_TRADES + 1)])
    monkeypatch.setattr(roster, "flag_counts", lambda *a, **k: {})
    assert roster.main() == 0
    assert "Wallet roster" in (tmp_path / "ROSTER.md").read_text()

"""Grading math (ROI, CLV) and the pre-registered per-category verdict."""

from tipoff import compute_report, grade_row, side_price, verdict

NOW = 1_780_000_000.0


def row(**overrides):
    base = {
        "id": "1", "ts": "2026-07-10T12:00:00Z", "platform": "kalshi",
        "market_id": "T", "title": "t", "category": "politics", "side": "yes",
        "entry_price": "0.6000", "stake_usd": "25", "score": "70",
        "signals": "s", "hours_to_close": "48.0", "status": "open",
        "last_price": "0.6000", "resolved_ts": "", "result": "",
        "roi": "", "clv": "",
    }
    base.update(overrides)
    return base


# --- grading -----------------------------------------------------------------

def test_win_roi():
    r = row(last_price="0.7500")
    grade_row(r, "yes", NOW)
    assert r["status"] == "won"
    # bought at 0.60, pays 1.00 -> +66.67% per dollar staked
    assert abs(float(r["roi"]) - (0.4 / 0.6)) < 1e-4


def test_loss_roi_is_minus_one():
    r = row()
    grade_row(r, "no", NOW)
    assert r["status"] == "lost"
    assert float(r["roi"]) == -1.0


def test_void_is_flat():
    r = row()
    grade_row(r, "void", NOW)
    assert r["status"] == "void"
    assert float(r["roi"]) == 0.0 and float(r["clv"]) == 0.0


def test_clv_positive_when_line_moved_our_way():
    # entered YES at 0.60; last observed price before resolution 0.75
    r = row(last_price="0.7500")
    grade_row(r, "yes", NOW)
    assert abs(float(r["clv"]) - 0.15) < 1e-9


def test_clv_negative_when_we_were_exit_liquidity():
    # entered at 0.60, line faded to 0.50 — late even though it WON
    r = row(last_price="0.5000")
    grade_row(r, "yes", NOW)
    assert r["status"] == "won"
    assert float(r["clv"]) < 0


def test_clv_independent_of_outcome():
    r = row(last_price="0.7500")
    grade_row(r, "no", NOW)  # lost the bet...
    assert r["status"] == "lost"
    assert float(r["clv"]) > 0  # ...but the signal still led the market


def test_side_price_flips_for_no():
    assert side_price("yes", 0.70) == 0.70
    assert abs(side_price("no", 0.70) - 0.30) < 1e-9


# --- verdict (pre-registered) ---------------------------------------------------

def test_verdict_insufficient_below_20_graded():
    assert verdict(19, avg_clv=0.10, avg_roi=0.5) == "INSUFFICIENT DATA"


def test_verdict_followable_needs_clv_and_roi():
    assert verdict(25, avg_clv=0.03, avg_roi=0.05) == "FOLLOWABLE"


def test_verdict_marginal_thin_clv():
    assert verdict(25, avg_clv=0.01, avg_roi=0.05).startswith("MARGINAL")


def test_verdict_positive_roi_but_no_clv_is_not_followable():
    # lucky wins without line movement = not a repeatable edge
    assert verdict(25, avg_clv=-0.01, avg_roi=0.10).startswith("NOT FOLLOWABLE")


# --- per-category report ---------------------------------------------------------

def test_report_buckets_by_category():
    rows = [
        row(category="politics", status="won", roi="0.6667", clv="0.15"),
        row(category="politics", status="lost", roi="-1.0", clv="-0.05"),
        row(category="sports", status="open"),
    ]
    stats = compute_report(rows)
    assert stats["politics"]["graded"] == 2
    assert stats["politics"]["wins"] == 1
    assert abs(stats["politics"]["avg_clv"] - 0.05) < 1e-9
    assert stats["sports"]["open"] == 1
    assert stats["ALL"]["alerts"] == 3


def test_report_unknown_category_falls_into_other():
    stats = compute_report([row(category="weird")])
    assert stats["other"]["alerts"] == 1


def test_report_verdict_wired_through():
    rows = [row(status="won", roi="0.5", clv="0.05")] * 25
    stats = compute_report(rows)
    assert stats["politics"]["verdict"] == "FOLLOWABLE"
    assert compute_report([])["ALL"]["verdict"] == "INSUFFICIENT DATA"

"""Informed-flow reads (was the alert actually insider money, in hindsight)
and the end-of-calibration review."""

import tipoff
from tipoff import (
    grade_row, informed_read, read_counts, watch_reason_histogram,
    write_calibration_report,
)

NOW = 1_780_000_000.0


# --- informed_read quadrants: outcome vs information are different axes ------

def test_won_and_line_kept_moving_is_informed():
    assert informed_read(won=True, clv=0.12) == "informed-like"


def test_lost_but_line_moved_our_way_is_early_but_wrong():
    # a real signal with an unlucky outcome: evidence of informed flow
    assert informed_read(won=False, clv=0.08) == "early-but-wrong"


def test_line_moved_against_us_is_late_money_even_on_a_win():
    # winning by luck while being the exit liquidity is not skill
    assert informed_read(won=True, clv=-0.06) == "late-money"
    assert informed_read(won=False, clv=-0.06) == "late-money"


def test_small_moves_are_neutral():
    assert informed_read(won=True, clv=0.01) == "neutral"
    assert informed_read(won=False, clv=-0.01) == "neutral"


def test_grade_row_writes_the_read():
    row = {"entry_price": "0.6000", "side": "yes", "last_price": "0.7500",
           "resolved_ts": "", "result": "", "roi": "", "clv": "", "read": "",
           "status": "open"}
    grade_row(row, "yes", NOW)
    assert row["read"] == "informed-like"
    row2 = dict(row, status="open", last_price="0.5000")
    grade_row(row2, "yes", NOW)
    assert row2["read"] == "late-money"


def test_void_has_no_read():
    row = {"entry_price": "0.6000", "side": "yes", "last_price": "0.7500",
           "resolved_ts": "", "result": "", "roi": "", "clv": "",
           "read": "x", "status": "open"}
    grade_row(row, "void", NOW)
    assert row["read"] == ""


# --- histogram + counts --------------------------------------------------------

def test_watch_reason_histogram_groups_prefixes():
    rows = [{"reasons": "thin: $4 depth < $500; score 19 < 40"},
            {"reasons": "thin: $9 depth < $500"},
            {"reasons": "re-alert cooldown"}]
    hist = dict(watch_reason_histogram(rows))
    assert hist["thin"] == 2
    assert hist["score 19 < 40"] == 1
    assert hist["re-alert cooldown"] == 1


def test_read_counts():
    rows = [{"read": "informed-like"}, {"read": "informed-like"},
            {"read": "late-money"}, {"read": ""}]
    counts = read_counts(rows)
    assert counts["informed-like"] == 2 and counts["late-money"] == 1


# --- calibration review generation ----------------------------------------------

def ledger_row(status="won", clv="0.10", roi="0.5", read="informed-like",
               category="politics", triggers="volume_spike+large_trade"):
    return {"status": status, "clv": clv, "roi": roi, "read": read,
            "category": category, "triggers": triggers, "mode": "calib"}


def test_calibration_report_content_and_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(tipoff, "CALIB_REPORT_FILE",
                        tmp_path / "CALIBRATION.md")
    ledger = [
        ledger_row(),
        ledger_row(status="lost", clv="0.07", roi="-1.0",
                   read="early-but-wrong"),
        ledger_row(status="open", clv="", roi="", read=""),
    ]
    watch = [{"reasons": "thin: $4 depth < $500"},
             {"reasons": "thin: $2 depth < $500"},
             {"reasons": "score 30 < 40"}]
    research = [{"alerted": "M"}, {"alerted": "1"}, {"alerted": "0"}]
    meta = {"first_run_ts": NOW - 7 * 86400}

    summary = write_calibration_report(ledger, watch, research, meta,
                                       NOW)
    text = (tmp_path / "CALIBRATION.md").read_text()
    assert "# Calibration week review" in text
    assert "3 sim positions" in text and "1 additional MONITOR" in text
    assert "1W-1L" in text
    assert "| thin | 2 |" in text
    assert "1 informed-like" in text and "1 early-but-wrong" in text

    assert summary.startswith("📏 Calibration week complete")
    assert "1W-1L" in summary and "CALIBRATION.md" in summary


def test_calibration_report_handles_empty_week(tmp_path, monkeypatch):
    monkeypatch.setattr(tipoff, "CALIB_REPORT_FILE",
                        tmp_path / "CALIBRATION.md")
    summary = write_calibration_report([], [], [], {}, NOW)
    assert "0 sim alerts" in summary  # silent week still reports cleanly

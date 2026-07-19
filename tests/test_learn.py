"""Self-audit: grading the scanner's own signals against the move that
followed them."""

import learn
from learn import (
    FADE_EDGE, FOLLOW_EDGE, MIN_SAMPLES, build_report, forward_move,
    group_by, score_band, summarize, triggers_of, verdict_for,
)


def row(side="yes", yes_price="0.50", p_24h="0.55", **extra):
    base = {"side": side, "yes_price": yes_price, "p_24h": p_24h,
            "p_1h": p_24h, "p_6h": p_24h, "triggers": "volume_spike",
            "category": "politics", "score": "60", "alerted": "1",
            "insiderable": "normal"}
    base.update(extra)
    return base


# --- label maths -------------------------------------------------------------

def test_yes_side_label_is_price_gain():
    assert abs(forward_move(row()) - 0.05) < 1e-9


def test_no_side_label_is_inverted():
    # picked NO at 0.50, price fell to 0.45: that moved our way
    assert abs(forward_move(row(side="no", p_24h="0.45")) - 0.05) < 1e-9


def test_unfilled_and_na_horizons_are_skipped():
    assert forward_move(row(p_24h="")) is None
    assert forward_move(row(p_24h="na")) is None
    assert forward_move(row(p_24h=None)) is None


def test_malformed_numbers_are_skipped_not_crashed():
    assert forward_move(row(p_24h="abc")) is None
    assert forward_move(row(yes_price="")) is None


def test_horizon_is_selectable():
    r = row(p_1h="0.60", p_24h="0.40")
    assert abs(forward_move(r, "p_1h") - 0.10) < 1e-9
    assert abs(forward_move(r, "p_24h") + 0.10) < 1e-9


# --- bucket stats ------------------------------------------------------------

def test_flat_rows_do_not_count_against_hit_rate():
    # three moved our way, one against, six did not move at all
    s = summarize([0.02] * 3 + [-0.02] + [0.0] * 6)
    assert s["n"] == 10 and s["up"] == 3 and s["down"] == 1 and s["flat"] == 6
    assert abs(s["hit_rate"] - 0.75) < 1e-9  # 3 of the 4 that actually moved


def test_all_flat_bucket_reports_zero_hit_rate_safely():
    s = summarize([0.0] * 5)
    assert s["hit_rate"] == 0.0 and s["up"] == 0


def test_empty_bucket_is_safe():
    assert summarize([])["n"] == 0


# --- verdicts ----------------------------------------------------------------

def test_thin_samples_never_get_a_verdict():
    assert verdict_for(MIN_SAMPLES - 1, 0.99) == "INSUFFICIENT DATA"


def test_follow_fade_and_noise_bands():
    assert verdict_for(MIN_SAMPLES, FOLLOW_EDGE) == "FOLLOW"
    assert verdict_for(MIN_SAMPLES, FADE_EDGE).startswith("FADE")
    assert verdict_for(MIN_SAMPLES, 0.0).startswith("NOISE")


def test_fade_verdict_names_the_problem():
    assert "wrong way" in verdict_for(MIN_SAMPLES, -0.05)


# --- grouping ----------------------------------------------------------------

def test_multi_trigger_row_lands_in_every_trigger_bucket():
    assert triggers_of(row(triggers="volume_spike+price_jump")) == [
        "volume_spike", "price_jump"]
    buckets = group_by([row(triggers="volume_spike+price_jump")], triggers_of)
    assert set(buckets) == {"volume_spike", "price_jump"}


def test_rows_without_forward_price_are_excluded_from_grouping():
    buckets = group_by([row(p_24h=""), row()], lambda r: r["category"])
    assert buckets["politics"]["n"] == 1


def test_score_bands():
    assert score_band(row(score="90")) == "70+"
    assert score_band(row(score="60")) == "55 to 69"
    assert score_band(row(score="45")) == "40 to 54"
    assert score_band(row(score="10")) == "under 40"
    assert score_band(row(score="junk")) is None


def test_empty_keys_are_dropped():
    assert group_by([row(category="")], lambda r: r["category"]) == {}


# --- report ------------------------------------------------------------------

def test_report_contains_every_section_and_the_key_test():
    rows = [row() for _ in range(MIN_SAMPLES)] + \
           [row(alerted="0", p_24h="0.45") for _ in range(MIN_SAMPLES)]
    text = build_report(rows, "2026-07-19T00:00:00Z")
    assert "# What the scanner has learned about itself" in text
    assert "Does the alert logic select anything?" in text
    assert "Per trigger" in text and "Per score band" in text
    assert "alerted (passed gate and score)" in text
    assert "filtered out" in text
    # alerted rows gained 5c, filtered lost 5c, so alerted must read FOLLOW
    assert "FOLLOW" in text and "FADE" in text


def test_report_handles_no_usable_rows():
    text = build_report([row(p_24h="")], "2026-07-19T00:00:00Z")
    assert "0 with a filled 24h forward price" in text


def test_main_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(learn, "LEARNING_FILE", tmp_path / "LEARNING.md")
    monkeypatch.setattr(learn, "load_rows", lambda *a, **k: [row()])
    assert learn.main() == 0
    assert "learned about itself" in (tmp_path / "LEARNING.md").read_text()


def test_main_is_quiet_with_no_data(monkeypatch, capsys):
    monkeypatch.setattr(learn, "load_rows", lambda *a, **k: [])
    assert learn.main() == 0
    assert "nothing to learn" in capsys.readouterr().out

#!/usr/bin/env python3
"""
Tipoff self-audit: grade the scanner's own signals against what the price
actually did next.

The paper ledger only grades alerts that resolved, which is a handful of
rows. research/signals.csv is much bigger: every candidate the scanner
looked at, alerted or not, with the YES price captured 1h, 6h and 24h
later. That is a labeled training set the bot collected on its own, and
this module reads it.

For each row the label is the forward move in the direction the scanner
picked, which is the same thing as closing line value measured at a fixed
horizon:

    side = yes  ->  label = price_later - price_at_signal
    side = no   ->  label = price_at_signal - price_later

Positive means the market kept moving the way the signal pointed.

Nothing here changes thresholds by itself. It measures and reports, and
refuses to call anything until a bucket has enough samples. Auto-tuning on
a thin sample is how a scanner learns noise.

Run it standalone or let the hourly workflow call it:
    python learn.py
"""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESEARCH_FILE = ROOT / "research" / "signals.csv"
LEARNING_FILE = ROOT / "research" / "LEARNING.md"

HORIZONS = ("p_1h", "p_6h", "p_24h")
PRIMARY_HORIZON = "p_24h"

MIN_SAMPLES = 30        # below this a bucket gets no verdict
FOLLOW_EDGE = 0.010     # avg forward move >= +1.0c reads as a follow signal
FADE_EDGE = -0.010      # avg forward move <= -1.0c reads as a fade signal


def forward_move(row: dict, horizon: str = PRIMARY_HORIZON) -> float | None:
    """Forward move in the direction the scanner picked, or None when the
    horizon has not been filled yet (blank) or the market left the universe
    before it could be (the literal string 'na')."""
    later = row.get(horizon)
    if later in (None, "", "na"):
        return None
    try:
        return (float(later) - float(row["yes_price"])) * (
            1.0 if row.get("side") == "yes" else -1.0)
    except (ValueError, KeyError, TypeError):
        return None


def load_rows(path: Path = RESEARCH_FILE) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def summarize(values: list[float]) -> dict:
    """Stats for one bucket. Ties matter here: plenty of markets simply do
    not move inside the horizon, so a plain win rate would read those as
    losses and understate everything."""
    n = len(values)
    if n == 0:
        return {"n": 0, "avg": 0.0, "median": 0.0, "up": 0, "down": 0,
                "flat": 0, "hit_rate": 0.0, "verdict": "NO DATA"}
    up = sum(1 for v in values if v > 0.0005)
    down = sum(1 for v in values if v < -0.0005)
    flat = n - up - down
    moved = up + down
    avg = statistics.mean(values)
    return {
        "n": n,
        "avg": avg,
        "median": statistics.median(values),
        "up": up, "down": down, "flat": flat,
        "hit_rate": (up / moved) if moved else 0.0,
        "verdict": verdict_for(n, avg),
    }


def verdict_for(n: int, avg: float) -> str:
    """Pre-registered read. Sample size gates everything: a bucket with a
    great average and 12 rows tells us nothing."""
    if n < MIN_SAMPLES:
        return "INSUFFICIENT DATA"
    if avg >= FOLLOW_EDGE:
        return "FOLLOW"
    if avg <= FADE_EDGE:
        return "FADE (signal points the wrong way)"
    return "NOISE (no measurable edge)"


def group_by(rows: list[dict], key_fn, horizon: str = PRIMARY_HORIZON) -> dict:
    """Bucket forward moves by whatever key_fn returns. A key_fn may return
    a list so one row can land in several buckets, which is what triggers
    need since an alert usually carries more than one."""
    buckets: dict[str, list[float]] = {}
    for row in rows:
        move = forward_move(row, horizon)
        if move is None:
            continue
        keys = key_fn(row)
        if keys is None:
            continue
        if isinstance(keys, str):
            keys = [keys]
        for key in keys:
            if key:
                buckets.setdefault(key, []).append(move)
    return {k: summarize(v) for k, v in buckets.items()}


def score_band(row: dict) -> str | None:
    try:
        score = int(row.get("score") or 0)
    except ValueError:
        return None
    if score >= 70:
        return "70+"
    if score >= 55:
        return "55 to 69"
    if score >= 40:
        return "40 to 54"
    return "under 40"


ALERT_LABELS = {"1": "alerted (passed gate and score)",
                "M": "monitor (strong but gated)",
                "0": "filtered out"}


def triggers_of(row: dict) -> list[str]:
    return [t.strip() for t in (row.get("triggers") or "").split("+")
            if t.strip()]


CLOSE_BANDS = ("under 1 day", "1 to 3 days", "3 to 7 days",
               "1 to 4 weeks", "over a month")


def close_band(row: dict) -> str | None:
    """How long until the market resolved, at signal time. The strongest
    timing lever found in the data: near-resolution signals pay, far-out
    ones do not (informed money shows up when the event is imminent)."""
    try:
        h = float(row.get("hours_to_close") or 0)
    except ValueError:
        return None
    if h <= 0:
        return None
    if h < 24:
        return "under 1 day"
    if h < 72:
        return "1 to 3 days"
    if h < 168:
        return "3 to 7 days"
    if h < 720:
        return "1 to 4 weeks"
    return "over a month"


def table(title: str, buckets: dict, note: str = "") -> list[str]:
    """Render one section, best average first."""
    lines = [f"## {title}", ""]
    if note:
        lines += [note, ""]
    lines += ["| Bucket | Samples | Avg move | Median | Moved our way | Verdict |",
              "|---|---|---|---|---|---|"]
    for name, s in sorted(buckets.items(), key=lambda kv: -kv[1]["avg"]):
        if s["n"] == 0:
            continue
        hit = f"{s['hit_rate'] * 100:.0f}%" if (s["up"] + s["down"]) else "n/a"
        lines.append(
            f"| {name} | {s['n']} | {s['avg'] * 100:+.2f}c |"
            f" {s['median'] * 100:+.2f}c | {hit} | {s['verdict']} |")
    lines.append("")
    return lines


def build_report(rows: list[dict], generated_at: str) -> str:
    usable = [r for r in rows if forward_move(r) is not None]
    lines = [
        "# What the scanner has learned about itself",
        "",
        f"_Auto-generated {generated_at}. {len(rows)} candidates logged,"
        f" {len(usable)} with a filled 24h forward price._",
        "",
        "Every row is scored on the move that followed it, in the direction",
        "the scanner picked. Positive means the market kept going our way,",
        "which is the thing that actually matters for a follower. A bucket",
        f"needs {MIN_SAMPLES} samples before it gets a verdict, and nothing",
        "here changes a threshold on its own. Read it, then decide.",
        "",
        "Averages are in cents of probability. 'Moved our way' ignores rows",
        "where the price did not move at all, which is common in thin",
        "markets and would otherwise look like a loss.",
        "",
    ]
    lines += table(
        "Does the alert logic select anything?",
        group_by(rows, lambda r: ALERT_LABELS.get(r.get("alerted"))),
        "The one test that matters most. Alerted rows should beat filtered"
        " rows. If they do not, the gate and the score are decoration.")
    lines += table(
        "Per trigger",
        group_by(rows, triggers_of),
        "A trigger that reads FADE is pointing the wrong way and is a"
        " candidate for inverting or dropping.")
    lines += table("Per category", group_by(rows, lambda r: r.get("category")))
    lines += table(
        "Per score band",
        group_by(rows, score_band),
        "These should improve as the score rises. If they do not, the point"
        " weights are wrong.")
    lines += table(
        "Per insiderability tier",
        group_by(rows, lambda r: r.get("insiderable")),
        "'high' means a market that resolves on a private human decision.")
    lines += table(
        "Per time-to-resolution (the accurate-time-to-bet table)",
        {b: group_by(rows, close_band).get(b, summarize([]))
         for b in CLOSE_BANDS},
        "Sorted by average, but read it in time order too. The strongest"
        " timing lever in the data: near-resolution signals pay, far-out ones"
        " do not. Informed money shows up when the event is imminent; a spike"
        " months out is rumor churn. This is why the gate now caps at 30 days.")

    lines += ["## Horizon check", "",
              "| Horizon | Samples | Avg move | Moved our way |",
              "|---|---|---|---|"]
    for horizon in HORIZONS:
        alerted = [r for r in rows if r.get("alerted") == "1"]
        s = summarize([m for r in alerted
                       if (m := forward_move(r, horizon)) is not None])
        hit = f"{s['hit_rate'] * 100:.0f}%" if (s["up"] + s["down"]) else "n/a"
        lines.append(f"| {horizon} (alerted only) | {s['n']} |"
                     f" {s['avg'] * 100:+.2f}c | {hit} |")
    lines += ["", "## How to act on this", "",
              "1. A trigger with a FADE verdict and a real sample is the",
              "   clearest finding available. Either invert it or drop it.",
              "2. If score bands do not climb, rebalance the points in",
              "   config.py toward whichever triggers actually earn.",
              "3. Anything still reading INSUFFICIENT DATA stays untouched.",
              "   Waiting is cheaper than learning noise.",
              ""]
    return "\n".join(lines)


def main() -> int:
    from datetime import datetime, timezone
    rows = load_rows()
    if not rows:
        print("no research data yet, nothing to learn from")
        return 0
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    LEARNING_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEARNING_FILE.write_text(build_report(rows, stamp))
    usable = sum(1 for r in rows if forward_move(r) is not None)
    print(f"self-audit written to {LEARNING_FILE.name}"
          f" ({usable} labeled rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

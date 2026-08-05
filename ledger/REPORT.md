# Tipoff: sim-trading report

_Auto-generated 2026-08-05T10:44:26Z. 300 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 8 | 8 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| politics | 30 | 30 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| sports | 0 | 0 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| crypto | 18 | 18 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| other | 72 | 70 | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |
| ALL | 128 | 126 | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 0 informed-like · 0 early-but-wrong (real signal, unlucky outcome) · 0 late-money · 2 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| price_jump | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |
| volume_spike | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |

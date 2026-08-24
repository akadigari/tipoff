# Tipoff: sim-trading report

_Auto-generated 2026-08-24T07:14:21Z. 488 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 11 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| politics | 67 | 67 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| sports | 4 | 4 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| crypto | 83 | 83 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| other | 151 | 148 | 3 | 33% | -56.1% | +4.0c | INSUFFICIENT DATA |
| ALL | 316 | 313 | 3 | 33% | -56.1% | +4.0c | INSUFFICIENT DATA |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 0 informed-like · 0 early-but-wrong (real signal, unlucky outcome) · 0 late-money · 3 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| price_jump | 3 | 33% | -56.1% | +4.0c | INSUFFICIENT DATA |
| volume_spike | 3 | 33% | -56.1% | +4.0c | INSUFFICIENT DATA |
| no_public_news | 1 | 100% | +31.6% | +3.0c | INSUFFICIENT DATA |

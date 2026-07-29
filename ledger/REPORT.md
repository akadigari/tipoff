# Tipoff: sim-trading report

_Auto-generated 2026-07-29T21:07:55Z. 251 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 5 | 5 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| politics | 19 | 19 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| sports | 0 | 0 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| crypto | 9 | 9 | 0 | 0% | +0.0% | +0.0c | INSUFFICIENT DATA |
| other | 46 | 44 | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |
| ALL | 79 | 77 | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 0 informed-like · 0 early-but-wrong (real signal, unlucky outcome) · 0 late-money · 2 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| price_jump | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |
| volume_spike | 2 | 0% | -100.0% | +4.5c | INSUFFICIENT DATA |

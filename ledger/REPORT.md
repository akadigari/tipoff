# Tipoff: sim-trading report

_Auto-generated 2026-09-01T04:56:05Z. 520 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 71 | 17 | 54 | 41% | -27.1% | -9.9c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 94 | 3 | 91 | 53% | +51.9% | +7.2c | FOLLOWABLE |
| other | 168 | 45 | 123 | 51% | +37.0% | +5.5c | FOLLOWABLE |
| ALL | 348 | 65 | 283 | 49% | +27.4% | +3.3c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 135 informed-like · 2 early-but-wrong (real signal, unlucky outcome) · 137 late-money · 9 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| large_trade | 241 | 49% | +27.0% | +3.7c | FOLLOWABLE |
| volume_spike | 238 | 48% | +30.5% | +3.9c | FOLLOWABLE |
| repeat_actor | 201 | 48% | +22.3% | +2.6c | FOLLOWABLE |
| price_jump | 149 | 54% | +18.3% | +1.6c | MARGINAL: edge exists but thin |
| within_trader | 93 | 44% | -3.4% | +0.6c | MARGINAL: edge exists but thin |
| no_public_news | 77 | 56% | +42.2% | +9.7c | FOLLOWABLE |
| insiderable | 25 | 28% | -49.2% | -16.8c | NOT FOLLOWABLE: following is late money |
| thin_market | 15 | 47% | -6.4% | -8.5c | INSUFFICIENT DATA |
| price_impact | 11 | 55% | +22.2% | +1.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

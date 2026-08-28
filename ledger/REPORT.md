# Tipoff: sim-trading report

_Auto-generated 2026-08-28T20:10:09Z. 508 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 70 | 20 | 50 | 42% | -25.9% | -8.5c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 91 | 29 | 62 | 60% | +90.4% | +12.4c | FOLLOWABLE |
| other | 160 | 53 | 107 | 56% | +52.7% | +7.9c | FOLLOWABLE |
| ALL | 336 | 102 | 234 | 53% | +42.3% | +5.6c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 121 informed-like · 1 early-but-wrong (real signal, unlucky outcome) · 105 late-money · 7 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| volume_spike | 196 | 53% | +47.2% | +6.3c | FOLLOWABLE |
| large_trade | 195 | 53% | +44.3% | +6.7c | FOLLOWABLE |
| repeat_actor | 163 | 53% | +40.7% | +6.0c | FOLLOWABLE |
| price_jump | 130 | 54% | +21.3% | +1.5c | MARGINAL: edge exists but thin |
| within_trader | 69 | 49% | +11.4% | +3.3c | FOLLOWABLE |
| no_public_news | 69 | 59% | +53.7% | +12.4c | FOLLOWABLE |
| insiderable | 23 | 30% | -44.8% | -11.2c | NOT FOLLOWABLE: following is late money |
| thin_market | 13 | 54% | +8.0% | -0.8c | INSUFFICIENT DATA |
| price_impact | 10 | 60% | +34.4% | +4.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

# Tipoff: sim-trading report

_Auto-generated 2026-08-30T13:45:48Z. 515 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 71 | 19 | 52 | 42% | -24.3% | -7.2c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 92 | 30 | 62 | 60% | +90.4% | +12.4c | FOLLOWABLE |
| other | 165 | 56 | 109 | 56% | +51.6% | +8.1c | FOLLOWABLE |
| ALL | 343 | 105 | 238 | 53% | +41.6% | +5.9c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 123 informed-like · 1 early-but-wrong (real signal, unlucky outcome) · 106 late-money · 8 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| large_trade | 199 | 53% | +43.4% | +7.0c | FOLLOWABLE |
| volume_spike | 197 | 53% | +47.3% | +6.5c | FOLLOWABLE |
| repeat_actor | 165 | 53% | +40.0% | +6.2c | FOLLOWABLE |
| price_jump | 133 | 53% | +20.3% | +1.8c | MARGINAL: edge exists but thin |
| within_trader | 72 | 49% | +10.0% | +3.9c | FOLLOWABLE |
| no_public_news | 70 | 60% | +54.0% | +12.8c | FOLLOWABLE |
| insiderable | 23 | 30% | -44.8% | -11.2c | NOT FOLLOWABLE: following is late money |
| thin_market | 13 | 54% | +8.0% | -0.8c | INSUFFICIENT DATA |
| price_impact | 10 | 60% | +34.4% | +4.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

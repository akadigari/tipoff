# Tipoff: sim-trading report

_Auto-generated 2026-08-26T23:21:37Z. 506 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 70 | 21 | 49 | 43% | -24.4% | -7.8c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 90 | 30 | 60 | 60% | +85.9% | +11.9c | FOLLOWABLE |
| other | 159 | 54 | 105 | 55% | +50.4% | +7.2c | FOLLOWABLE |
| ALL | 334 | 105 | 229 | 53% | +40.1% | +5.3c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 118 informed-like · 1 early-but-wrong (real signal, unlucky outcome) · 103 late-money · 7 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| volume_spike | 192 | 53% | +46.1% | +6.2c | FOLLOWABLE |
| large_trade | 190 | 53% | +41.7% | +6.3c | FOLLOWABLE |
| repeat_actor | 159 | 53% | +36.6% | +5.2c | FOLLOWABLE |
| price_jump | 128 | 53% | +18.8% | +0.8c | MARGINAL: edge exists but thin |
| no_public_news | 69 | 59% | +53.7% | +12.4c | FOLLOWABLE |
| within_trader | 68 | 50% | +13.1% | +4.0c | FOLLOWABLE |
| insiderable | 23 | 30% | -44.8% | -11.2c | NOT FOLLOWABLE: following is late money |
| thin_market | 13 | 54% | +8.0% | -0.8c | INSUFFICIENT DATA |
| price_impact | 10 | 60% | +34.4% | +4.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

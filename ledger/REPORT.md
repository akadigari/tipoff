# Tipoff: sim-trading report

_Auto-generated 2026-08-26T07:02:43Z. 500 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 70 | 22 | 48 | 42% | -25.5% | -8.5c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 88 | 29 | 59 | 59% | +82.5% | +10.8c | FOLLOWABLE |
| other | 155 | 50 | 105 | 55% | +50.4% | +7.2c | FOLLOWABLE |
| ALL | 328 | 101 | 227 | 53% | +39.1% | +4.9c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 116 informed-like · 1 early-but-wrong (real signal, unlucky outcome) · 103 late-money · 7 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| volume_spike | 190 | 52% | +45.0% | +5.8c | FOLLOWABLE |
| large_trade | 188 | 53% | +40.5% | +5.9c | FOLLOWABLE |
| repeat_actor | 157 | 52% | +35.1% | +4.7c | FOLLOWABLE |
| price_jump | 128 | 53% | +18.8% | +0.8c | MARGINAL: edge exists but thin |
| within_trader | 68 | 50% | +13.1% | +4.0c | FOLLOWABLE |
| no_public_news | 68 | 59% | +54.0% | +12.2c | FOLLOWABLE |
| insiderable | 23 | 30% | -44.8% | -11.2c | NOT FOLLOWABLE: following is late money |
| thin_market | 13 | 54% | +8.0% | -0.8c | INSUFFICIENT DATA |
| price_impact | 10 | 60% | +34.4% | +4.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

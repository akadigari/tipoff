# Tipoff: sim-trading report

_Auto-generated 2026-08-31T05:21:20Z. 517 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 71 | 17 | 54 | 41% | -27.1% | -9.9c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 93 | 26 | 67 | 61% | +90.1% | +13.7c | FOLLOWABLE |
| other | 166 | 57 | 109 | 56% | +51.6% | +8.1c | FOLLOWABLE |
| ALL | 345 | 100 | 245 | 53% | +41.4% | +5.7c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 126 informed-like · 2 early-but-wrong (real signal, unlucky outcome) · 108 late-money · 9 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| large_trade | 206 | 53% | +43.1% | +6.7c | FOLLOWABLE |
| volume_spike | 202 | 53% | +47.3% | +6.7c | FOLLOWABLE |
| repeat_actor | 170 | 54% | +38.9% | +6.0c | FOLLOWABLE |
| price_jump | 138 | 54% | +21.7% | +2.1c | FOLLOWABLE |
| within_trader | 74 | 49% | +9.8% | +3.9c | FOLLOWABLE |
| no_public_news | 70 | 60% | +54.0% | +12.8c | FOLLOWABLE |
| insiderable | 25 | 28% | -49.2% | -16.8c | NOT FOLLOWABLE: following is late money |
| thin_market | 13 | 54% | +8.0% | -0.8c | INSUFFICIENT DATA |
| price_impact | 10 | 60% | +34.4% | +4.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

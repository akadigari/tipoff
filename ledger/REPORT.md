# Tipoff: sim-trading report

_Auto-generated 2026-09-01T13:27:04Z. 521 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 71 | 15 | 56 | 41% | -25.0% | -9.9c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 94 | 3 | 91 | 53% | +51.9% | +7.2c | FOLLOWABLE |
| other | 169 | 35 | 134 | 50% | +31.0% | +4.8c | FOLLOWABLE |
| ALL | 349 | 53 | 296 | 49% | +25.1% | +2.9c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 140 informed-like · 2 early-but-wrong (real signal, unlucky outcome) · 145 late-money · 9 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| large_trade | 253 | 48% | +24.8% | +3.4c | FOLLOWABLE |
| volume_spike | 250 | 48% | +28.1% | +3.8c | FOLLOWABLE |
| repeat_actor | 213 | 48% | +20.0% | +2.3c | FOLLOWABLE |
| price_jump | 153 | 52% | +15.2% | -0.1c | NOT FOLLOWABLE: following is late money |
| within_trader | 95 | 44% | -2.7% | +1.2c | MARGINAL: edge exists but thin |
| no_public_news | 81 | 57% | +41.6% | +9.4c | FOLLOWABLE |
| insiderable | 25 | 28% | -49.2% | -16.8c | NOT FOLLOWABLE: following is late money |
| thin_market | 16 | 50% | +4.2% | -4.1c | INSUFFICIENT DATA |
| price_impact | 11 | 55% | +22.2% | +1.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

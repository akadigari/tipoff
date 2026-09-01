# Tipoff: sim-trading report

_Auto-generated 2026-09-01T23:14:23Z. 524 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 72 | 16 | 56 | 41% | -25.0% | -9.9c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 94 | 3 | 91 | 53% | +51.9% | +7.2c | FOLLOWABLE |
| other | 171 | 30 | 141 | 49% | +26.6% | +3.9c | FOLLOWABLE |
| ALL | 352 | 49 | 303 | 49% | +23.1% | +2.6c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 142 informed-like · 3 early-but-wrong (real signal, unlucky outcome) · 149 late-money · 9 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| large_trade | 260 | 48% | +22.5% | +3.0c | FOLLOWABLE |
| volume_spike | 255 | 48% | +26.7% | +3.4c | FOLLOWABLE |
| repeat_actor | 220 | 47% | +17.5% | +1.9c | MARGINAL: edge exists but thin |
| price_jump | 157 | 51% | +12.3% | -0.5c | NOT FOLLOWABLE: following is late money |
| within_trader | 99 | 43% | -5.1% | +1.1c | MARGINAL: edge exists but thin |
| no_public_news | 84 | 56% | +38.2% | +9.2c | FOLLOWABLE |
| insiderable | 25 | 28% | -49.2% | -16.8c | NOT FOLLOWABLE: following is late money |
| thin_market | 17 | 53% | +6.6% | -2.3c | INSUFFICIENT DATA |
| price_impact | 11 | 55% | +22.2% | +1.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 4 | 75% | +281.5% | +37.6c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

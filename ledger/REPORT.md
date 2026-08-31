# Tipoff: sim-trading report

_Auto-generated 2026-08-31T23:45:00Z. 520 alerts ledgered (172 from calibration week, excluded from the verdict stats below).

CLV = final observed price for our side minus entry price, in probability
points. Positive CLV means the market kept moving our way after the alert.
A category is only called FOLLOWABLE with >= 20 graded alerts, avg CLV
> +0.02 and positive avg ROI. See README for how to read this.

| Category | Alerts | Open | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|---|---|
| entertainment | 11 | 0 | 11 | 45% | -2.9% | +4.1c | INSUFFICIENT DATA |
| politics | 71 | 17 | 54 | 41% | -27.1% | -9.9c | NOT FOLLOWABLE: following is late money |
| sports | 4 | 0 | 4 | 50% | -6.1% | +20.0c | INSUFFICIENT DATA |
| crypto | 94 | 27 | 67 | 61% | +90.1% | +13.7c | FOLLOWABLE |
| other | 168 | 45 | 123 | 51% | +37.0% | +5.5c | FOLLOWABLE |
| ALL | 348 | 89 | 259 | 51% | +35.0% | +4.6c | FOLLOWABLE |

**Informed-flow reads** (was the alert actually informed money, judged by where the line went): 128 informed-like · 2 early-but-wrong (real signal, unlucky outcome) · 120 late-money · 9 neutral

## By trigger

A graded alert counts toward every signal it contained. This is
the follow-vs-fade table: a trigger with negative CLV is one to
fade or drop, whatever its win rate says.

| Trigger | Graded | Win% | Avg ROI | Avg CLV | Verdict |
|---|---|---|---|---|---|
| large_trade | 218 | 51% | +36.0% | +5.3c | FOLLOWABLE |
| volume_spike | 216 | 50% | +39.3% | +5.3c | FOLLOWABLE |
| repeat_actor | 181 | 51% | +31.3% | +4.4c | FOLLOWABLE |
| price_jump | 141 | 54% | +21.5% | +2.5c | FOLLOWABLE |
| within_trader | 80 | 46% | +3.6% | +2.2c | FOLLOWABLE |
| no_public_news | 77 | 56% | +42.2% | +9.7c | FOLLOWABLE |
| insiderable | 25 | 28% | -49.2% | -16.8c | NOT FOLLOWABLE: following is late money |
| thin_market | 15 | 47% | -6.4% | -8.5c | INSUFFICIENT DATA |
| price_impact | 10 | 60% | +34.4% | +4.3c | INSUFFICIENT DATA |
| cross_platform | 7 | 71% | +21.7% | +10.8c | INSUFFICIENT DATA |
| fresh_wallet | 3 | 67% | +360.3% | +41.5c | INSUFFICIENT DATA |
| chatter | 1 | 0% | -100.0% | -45.0c | INSUFFICIENT DATA |

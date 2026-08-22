# What the scanner has learned about itself

_Auto-generated 2026-08-22T05:36:11Z. 10000 candidates logged, 5441 with a filled 24h forward price._

Every row is scored on the move that followed it, in the direction
the scanner picked. Positive means the market kept going our way,
which is the thing that actually matters for a follower. A bucket
needs 30 samples before it gets a verdict, and nothing
here changes a threshold on its own. Read it, then decide.

Averages are in cents of probability. 'Moved our way' ignores rows
where the price did not move at all, which is common in thin
markets and would otherwise look like a loss.

## Does the alert logic select anything?

The one test that matters most. Alerted rows should beat filtered rows. If they do not, the gate and the score are decoration.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| alerted (passed gate and score) | 42 | +3.43c | +0.47c | 54% | FOLLOW |
| filtered out | 5221 | +0.00c | -0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 178 | -0.62c | -0.00c | 53% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 231 | +2.22c | +1.00c | 55% | FOLLOW |
| cross_platform | 104 | +0.89c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 725 | +0.17c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4809 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 743 | -0.19c | +0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 469 | -0.33c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1636 | -0.64c | +0.00c | 53% | NOISE (no measurable edge) |
| repeat_actor | 1194 | -0.75c | -0.00c | 55% | NOISE (no measurable edge) |
| thin_market | 41 | -0.89c | +0.05c | 57% | NOISE (no measurable edge) |
| fresh_wallet | 19 | -0.90c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 975 | +0.84c | +0.25c | 57% | NOISE (no measurable edge) |
| politics | 2241 | +0.09c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2138 | -0.39c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 87 | -1.86c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 696 | +0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3442 | +0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 521 | -0.05c | +0.00c | 56% | NOISE (no measurable edge) |
| 55 to 69 | 782 | -0.80c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4972 | +0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 469 | -0.33c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 48 | +4.60c | +0.00c | 48% | FOLLOW |
| 1 to 3 days | 285 | +0.91c | +0.35c | 56% | NOISE (no measurable edge) |
| 3 to 7 days | 231 | +0.79c | +0.20c | 52% | NOISE (no measurable edge) |
| over a month | 3455 | +0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1271 | -0.64c | -0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 84 | +1.80c | 59% |
| p_6h (alerted only) | 72 | +3.20c | 55% |
| p_24h (alerted only) | 42 | +3.43c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

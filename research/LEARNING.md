# What the scanner has learned about itself

_Auto-generated 2026-08-26T23:22:13Z. 10000 candidates logged, 5979 with a filled 24h forward price._

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
| alerted (passed gate and score) | 61 | +0.34c | -0.50c | 47% | NOISE (no measurable edge) |
| filtered out | 5703 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 215 | -1.19c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 55 | +1.38c | -0.00c | 44% | FOLLOW |
| insiderable | 521 | +0.23c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 328 | +0.07c | -0.93c | 47% | NOISE (no measurable edge) |
| volume_spike | 5236 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 868 | -0.17c | +0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.38c | -0.05c | 31% | INSUFFICIENT DATA |
| large_trade | 2010 | -0.44c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1483 | -0.59c | -0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 876 | -0.90c | -0.50c | 49% | NOISE (no measurable edge) |
| coordination | 8 | -1.09c | +0.03c | 50% | INSUFFICIENT DATA |
| chatter | 3 | -1.17c | -0.00c | 0% | INSUFFICIENT DATA |
| thin_market | 30 | -3.27c | +0.08c | 55% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1489 | +0.12c | +0.05c | 52% | NOISE (no measurable edge) |
| politics | 2067 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2327 | -0.27c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 96 | -1.06c | -1.00c | 34% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 760 | +0.22c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3592 | +0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 948 | -0.51c | +0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 679 | -0.72c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 521 | +0.23c | +0.00c | 50% | NOISE (no measurable edge) |
| normal | 5458 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 426 | +0.96c | +0.38c | 56% | NOISE (no measurable edge) |
| over a month | 3669 | -0.01c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 270 | -0.53c | +0.53c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1499 | -0.73c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 96 | +1.23c | 55% |
| p_6h (alerted only) | 84 | +2.76c | 54% |
| p_24h (alerted only) | 61 | +0.34c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

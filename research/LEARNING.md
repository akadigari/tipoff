# What the scanner has learned about itself

_Auto-generated 2026-08-24T17:39:00Z. 10000 candidates logged, 5705 with a filled 24h forward price._

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
| filtered out | 5440 | -0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 57 | -0.63c | -0.50c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 208 | -1.09c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 91 | +1.01c | +0.00c | 49% | FOLLOW |
| price_impact | 281 | +0.89c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 851 | -0.03c | -0.00c | 54% | NOISE (no measurable edge) |
| volume_spike | 5048 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 521 | -0.11c | -0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 16 | -0.16c | +0.00c | 46% | INSUFFICIENT DATA |
| price_jump | 765 | -0.46c | -0.10c | 49% | NOISE (no measurable edge) |
| large_trade | 1884 | -0.58c | -0.00c | 51% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1388 | -0.69c | -0.00c | 53% | NOISE (no measurable edge) |
| thin_market | 36 | -2.45c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1318 | +0.31c | +0.07c | 53% | NOISE (no measurable edge) |
| politics | 2090 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 92 | -0.35c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2205 | -0.45c | +0.00c | 45% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 743 | +0.24c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3437 | +0.11c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 636 | -0.40c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 889 | -0.80c | +0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5184 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 521 | -0.11c | -0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 39 | +4.85c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 228 | +1.38c | +0.30c | 53% | FOLLOW |
| over a month | 3551 | -0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 270 | -0.03c | +0.50c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1498 | -0.66c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.35c | 58% |
| p_6h (alerted only) | 82 | +1.87c | 51% |
| p_24h (alerted only) | 57 | -0.63c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

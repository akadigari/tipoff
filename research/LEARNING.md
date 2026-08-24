# What the scanner has learned about itself

_Auto-generated 2026-08-24T19:37:26Z. 10000 candidates logged, 5700 with a filled 24h forward price._

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
| filtered out | 5434 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 57 | -0.63c | -0.50c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 209 | -1.09c | +0.00c | 52% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 89 | +0.91c | -0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 281 | +0.86c | +0.00c | 49% | NOISE (no measurable edge) |
| volume_spike | 5048 | -0.04c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 849 | -0.05c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 523 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 16 | -0.16c | +0.00c | 46% | INSUFFICIENT DATA |
| price_jump | 760 | -0.46c | -0.38c | 49% | NOISE (no measurable edge) |
| large_trade | 1886 | -0.56c | +0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1391 | -0.66c | -0.00c | 53% | NOISE (no measurable edge) |
| thin_market | 34 | -2.69c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1320 | +0.32c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2091 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 91 | -0.27c | +0.00c | 46% | NOISE (no measurable edge) |
| other | 2198 | -0.41c | +0.00c | 45% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 741 | +0.26c | -0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3433 | +0.13c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 632 | -0.42c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 894 | -0.77c | +0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5177 | -0.05c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 523 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 38 | +5.18c | +0.00c | 48% | FOLLOW |
| 3 to 7 days | 226 | +1.32c | +0.23c | 52% | FOLLOW |
| 1 to 3 days | 267 | +0.32c | +0.50c | 56% | NOISE (no measurable edge) |
| over a month | 3561 | +0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1490 | -0.66c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 95 | +1.27c | 56% |
| p_6h (alerted only) | 82 | +1.87c | 51% |
| p_24h (alerted only) | 57 | -0.63c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

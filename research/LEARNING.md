# What the scanner has learned about itself

_Auto-generated 2026-08-15T04:40:43Z. 10000 candidates logged, 5554 with a filled 24h forward price._

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
| alerted (passed gate and score) | 71 | +0.64c | +1.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5275 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 208 | -1.07c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 69 | +1.65c | +0.50c | 68% | FOLLOW |
| cross_platform | 161 | +1.36c | +0.00c | 50% | FOLLOW |
| repeat_actor | 1273 | +0.88c | +0.15c | 59% | NOISE (no measurable edge) |
| within_trader | 744 | +0.82c | +0.10c | 59% | NOISE (no measurable edge) |
| large_trade | 1823 | +0.76c | +0.10c | 58% | NOISE (no measurable edge) |
| volume_spike | 4782 | +0.26c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 484 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 24 | -0.01c | -0.03c | 45% | INSUFFICIENT DATA |
| price_jump | 886 | -0.14c | -0.00c | 51% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 256 | -0.81c | -0.65c | 45% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 559 | +0.32c | -0.00c | 53% | NOISE (no measurable edge) |
| politics | 2432 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2418 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 126 | -0.20c | +0.00c | 43% | NOISE (no measurable edge) |
| sports | 19 | -4.58c | -2.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 811 | +0.80c | +0.10c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 795 | +0.41c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 558 | +0.24c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3390 | -0.05c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5070 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| high | 484 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 64 | +1.53c | +0.33c | 53% | FOLLOW |
| 3 to 7 days | 415 | +1.45c | +0.30c | 57% | FOLLOW |
| 1 to 4 weeks | 1263 | +0.52c | +0.05c | 54% | NOISE (no measurable edge) |
| 1 to 3 days | 325 | +0.23c | +0.30c | 55% | NOISE (no measurable edge) |
| over a month | 3386 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 99 | -0.18c | 45% |
| p_6h (alerted only) | 95 | -0.24c | 45% |
| p_24h (alerted only) | 71 | +0.64c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

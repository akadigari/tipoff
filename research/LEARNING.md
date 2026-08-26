# What the scanner has learned about itself

_Auto-generated 2026-08-26T14:55:39Z. 10000 candidates logged, 5745 with a filled 24h forward price._

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
| alerted (passed gate and score) | 60 | +0.33c | -0.50c | 47% | NOISE (no measurable edge) |
| filtered out | 5479 | -0.03c | -0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 206 | -1.11c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 53 | +1.43c | -0.00c | 45% | FOLLOW |
| price_impact | 314 | +0.29c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 500 | +0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| volume_spike | 5024 | -0.02c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 831 | -0.16c | -0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1928 | -0.41c | +0.00c | 52% | NOISE (no measurable edge) |
| fresh_wallet | 16 | -0.46c | -0.05c | 25% | INSUFFICIENT DATA |
| repeat_actor | 1418 | -0.55c | -0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 840 | -0.70c | +0.00c | 50% | NOISE (no measurable edge) |
| coordination | 8 | -1.09c | +0.03c | 50% | INSUFFICIENT DATA |
| chatter | 2 | -1.75c | -1.75c | 0% | INSUFFICIENT DATA |
| thin_market | 31 | -3.21c | +0.05c | 53% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1456 | +0.16c | +0.00c | 52% | NOISE (no measurable edge) |
| politics | 1960 | +0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2236 | -0.28c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 93 | -1.05c | -1.00c | 36% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 743 | +0.23c | -0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3446 | +0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 911 | -0.49c | -0.00c | 52% | NOISE (no measurable edge) |
| 70+ | 645 | -0.65c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 500 | +0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| normal | 5245 | -0.09c | -0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 342 | +1.24c | +0.27c | 53% | FOLLOW |
| over a month | 3529 | -0.02c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 259 | -0.22c | +0.95c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1494 | -0.67c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 92 | +1.11c | 54% |
| p_6h (alerted only) | 81 | +2.81c | 55% |
| p_24h (alerted only) | 60 | +0.33c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

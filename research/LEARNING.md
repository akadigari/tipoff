# What the scanner has learned about itself

_Auto-generated 2026-08-26T16:25:22Z. 10000 candidates logged, 5793 with a filled 24h forward price._

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
| filtered out | 5527 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 206 | -1.11c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 53 | +1.43c | -0.00c | 45% | FOLLOW |
| price_impact | 316 | +0.18c | -0.68c | 47% | NOISE (no measurable edge) |
| insiderable | 503 | +0.12c | -0.00c | 49% | NOISE (no measurable edge) |
| volume_spike | 5063 | -0.01c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 838 | -0.16c | -0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1947 | -0.43c | -0.00c | 52% | NOISE (no measurable edge) |
| fresh_wallet | 16 | -0.46c | -0.05c | 25% | INSUFFICIENT DATA |
| repeat_actor | 1436 | -0.56c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 846 | -0.83c | -0.05c | 49% | NOISE (no measurable edge) |
| coordination | 8 | -1.09c | +0.03c | 50% | INSUFFICIENT DATA |
| chatter | 2 | -1.75c | -1.75c | 0% | INSUFFICIENT DATA |
| thin_market | 31 | -3.21c | +0.05c | 53% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1469 | +0.14c | +0.05c | 52% | NOISE (no measurable edge) |
| politics | 1983 | +0.04c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2248 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 93 | -1.06c | -1.00c | 35% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 741 | +0.19c | -0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3479 | +0.08c | -0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 920 | -0.50c | +0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 653 | -0.65c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 503 | +0.12c | -0.00c | 49% | NOISE (no measurable edge) |
| normal | 5290 | -0.10c | -0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 370 | +0.94c | +0.30c | 54% | NOISE (no measurable edge) |
| over a month | 3554 | -0.02c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 261 | -0.22c | +0.95c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1488 | -0.68c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.08c | 54% |
| p_6h (alerted only) | 82 | +2.73c | 54% |
| p_24h (alerted only) | 60 | +0.33c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

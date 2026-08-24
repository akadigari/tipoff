# What the scanner has learned about itself

_Auto-generated 2026-08-24T04:55:59Z. 10000 candidates logged, 5761 with a filled 24h forward price._

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
| alerted (passed gate and score) | 55 | +0.51c | +0.35c | 53% | NOISE (no measurable edge) |
| filtered out | 5500 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 206 | -1.18c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 89 | +1.14c | -0.00c | 53% | FOLLOW |
| price_impact | 272 | +1.06c | +0.00c | 49% | FOLLOW |
| volume_spike | 5098 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 847 | -0.12c | -0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 532 | -0.19c | +0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 782 | -0.35c | -0.10c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.36c | -0.00c | 43% | INSUFFICIENT DATA |
| large_trade | 1851 | -0.57c | +0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1361 | -0.67c | -0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 44 | -1.78c | +0.03c | 55% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1248 | +0.38c | +0.08c | 53% | NOISE (no measurable edge) |
| politics | 2134 | +0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2278 | -0.42c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 101 | -2.51c | +0.00c | 45% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3515 | +0.11c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 737 | +0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 616 | -0.28c | +0.00c | 55% | NOISE (no measurable edge) |
| 55 to 69 | 893 | -0.80c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5229 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 532 | -0.19c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 43 | +3.84c | -0.00c | 46% | FOLLOW |
| 3 to 7 days | 235 | +0.85c | +0.40c | 54% | NOISE (no measurable edge) |
| over a month | 3598 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 306 | -0.37c | +0.25c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1446 | -0.51c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 95 | +1.34c | 59% |
| p_6h (alerted only) | 83 | +1.78c | 50% |
| p_24h (alerted only) | 55 | +0.51c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

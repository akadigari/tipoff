# What the scanner has learned about itself

_Auto-generated 2026-08-25T14:56:45Z. 10000 candidates logged, 5646 with a filled 24h forward price._

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
| filtered out | 5386 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 55 | -0.76c | -0.50c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 205 | -0.84c | +0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 75 | +1.07c | -0.00c | 46% | FOLLOW |
| price_impact | 293 | +0.43c | -0.85c | 47% | NOISE (no measurable edge) |
| within_trader | 826 | -0.02c | -0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4974 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 526 | -0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 783 | -0.38c | +0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 14 | -0.40c | -0.05c | 33% | INSUFFICIENT DATA |
| large_trade | 1852 | -0.47c | +0.00c | 53% | NOISE (no measurable edge) |
| repeat_actor | 1377 | -0.55c | +0.00c | 54% | NOISE (no measurable edge) |
| coordination | 7 | -1.07c | +0.25c | 67% | INSUFFICIENT DATA |
| thin_market | 33 | -2.90c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1349 | +0.22c | +0.05c | 53% | NOISE (no measurable edge) |
| politics | 1993 | +0.03c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2211 | -0.29c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 93 | -0.85c | -0.00c | 41% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 740 | +0.19c | +0.00c | 50% | NOISE (no measurable edge) |
| under 40 | 3402 | +0.07c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 639 | -0.38c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 865 | -0.57c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 526 | -0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| normal | 5120 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 33 | +5.23c | +0.00c | 45% | FOLLOW |
| 3 to 7 days | 230 | +1.24c | +0.20c | 52% | FOLLOW |
| 1 to 3 days | 245 | +0.02c | +0.55c | 54% | NOISE (no measurable edge) |
| over a month | 3509 | +0.02c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1517 | -0.65c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.04c | 55% |
| p_6h (alerted only) | 83 | +2.78c | 54% |
| p_24h (alerted only) | 55 | -0.76c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

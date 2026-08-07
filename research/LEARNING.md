# What the scanner has learned about itself

_Auto-generated 2026-08-07T05:47:24Z. 10000 candidates logged, 6050 with a filled 24h forward price._

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
| alerted (passed gate and score) | 83 | -0.23c | -0.20c | 47% | NOISE (no measurable edge) |
| filtered out | 5724 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 243 | -0.67c | -0.00c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| cross_platform | 145 | +0.44c | +0.00c | 47% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 5034 | -0.22c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2103 | -0.28c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1453 | -0.34c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 20 | -0.40c | +0.07c | 53% | INSUFFICIENT DATA |
| insiderable | 607 | -0.64c | -0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1191 | -0.82c | -0.50c | 48% | NOISE (no measurable edge) |
| within_trader | 873 | -0.93c | -0.00c | 53% | NOISE (no measurable edge) |
| thin_market | 43 | -1.03c | -0.00c | 49% | FADE (signal points the wrong way) |
| price_impact | 291 | -1.04c | -0.75c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 535 | +0.21c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2452 | -0.14c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 369 | -0.39c | +0.00c | 46% | NOISE (no measurable edge) |
| other | 2672 | -0.57c | +0.00c | 48% | NOISE (no measurable edge) |
| sports | 22 | -4.25c | -3.50c | 25% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 865 | -0.22c | -0.00c | 51% | NOISE (no measurable edge) |
| 55 to 69 | 901 | -0.24c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3625 | -0.24c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 659 | -1.10c | +0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5443 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 607 | -0.64c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 570 | +0.56c | +0.38c | 53% | NOISE (no measurable edge) |
| over a month | 3993 | -0.25c | -0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 957 | -0.26c | -0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 395 | -2.34c | -0.20c | 48% | FADE (signal points the wrong way) |
| under 1 day | 38 | -4.34c | +0.03c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.46c | 46% |
| p_6h (alerted only) | 106 | -0.72c | 45% |
| p_24h (alerted only) | 83 | -0.23c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

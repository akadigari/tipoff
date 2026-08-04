# What the scanner has learned about itself

_Auto-generated 2026-08-04T21:22:13Z. 10000 candidates logged, 5806 with a filled 24h forward price._

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
| alerted (passed gate and score) | 75 | -0.13c | -0.20c | 47% | NOISE (no measurable edge) |
| filtered out | 5498 | -0.38c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 233 | -0.67c | -0.00c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 19 | +2.98c | +0.65c | 61% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4804 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2051 | -0.38c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1419 | -0.43c | -0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 119 | -0.46c | -0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 284 | -0.50c | -0.30c | 48% | NOISE (no measurable edge) |
| insiderable | 612 | -0.63c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 864 | -0.70c | -0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 1180 | -1.00c | -1.00c | 46% | NOISE (no measurable edge) |
| thin_market | 44 | -1.40c | -0.02c | 43% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 515 | +0.36c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2314 | -0.18c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 370 | -0.28c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2584 | -0.73c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 23 | -1.76c | -2.00c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3451 | -0.27c | +0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 874 | -0.29c | -0.00c | 53% | NOISE (no measurable edge) |
| 40 to 54 | 821 | -0.56c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 660 | -0.95c | -0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5194 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 612 | -0.63c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 552 | +0.49c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3794 | -0.31c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 927 | -0.66c | -0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 397 | -1.80c | -0.30c | 47% | FADE (signal points the wrong way) |
| under 1 day | 38 | -2.30c | +0.65c | 58% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 101 | +0.36c | 42% |
| p_6h (alerted only) | 92 | -0.90c | 45% |
| p_24h (alerted only) | 75 | -0.13c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

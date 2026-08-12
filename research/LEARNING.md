# What the scanner has learned about itself

_Auto-generated 2026-08-12T02:36:44Z. 10000 candidates logged, 5688 with a filled 24h forward price._

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
| alerted (passed gate and score) | 83 | +0.87c | +0.15c | 52% | NOISE (no measurable edge) |
| filtered out | 5359 | +0.08c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 246 | -0.63c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 169 | +0.98c | +0.00c | 50% | NOISE (no measurable edge) |
| thin_market | 72 | +0.94c | +0.37c | 62% | NOISE (no measurable edge) |
| fresh_wallet | 22 | +0.92c | -0.05c | 48% | INSUFFICIENT DATA |
| repeat_actor | 1377 | +0.52c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1963 | +0.46c | +0.05c | 57% | NOISE (no measurable edge) |
| price_jump | 896 | +0.23c | -0.00c | 50% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| within_trader | 840 | +0.11c | +0.10c | 58% | NOISE (no measurable edge) |
| volume_spike | 4895 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| insiderable | 505 | -0.24c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 259 | -0.85c | -0.50c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2334 | +0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2640 | +0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 498 | +0.03c | -0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 188 | -0.53c | -0.03c | 43% | NOISE (no measurable edge) |
| sports | 28 | -4.79c | -4.25c | 26% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 830 | +0.57c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 802 | +0.43c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3440 | -0.08c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 616 | -0.30c | -0.00c | 57% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5183 | +0.09c | -0.00c | 50% | NOISE (no measurable edge) |
| high | 505 | -0.24c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 371 | +1.75c | +0.35c | 57% | FOLLOW |
| 1 to 4 weeks | 1229 | +0.54c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3550 | -0.18c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 379 | -0.75c | +0.05c | 51% | NOISE (no measurable edge) |
| under 1 day | 72 | -3.44c | +0.03c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 114 | +0.54c | 47% |
| p_6h (alerted only) | 113 | -1.21c | 41% |
| p_24h (alerted only) | 83 | +0.87c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

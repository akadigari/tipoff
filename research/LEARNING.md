# What the scanner has learned about itself

_Auto-generated 2026-08-04T03:30:27Z. 10000 candidates logged, 5908 with a filled 24h forward price._

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
| alerted (passed gate and score) | 69 | +0.00c | -1.00c | 46% | NOISE (no measurable edge) |
| filtered out | 5600 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 239 | -0.53c | -0.00c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 18 | +2.57c | +0.40c | 59% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 13 | +0.82c | +2.00c | 75% | INSUFFICIENT DATA |
| large_trade | 2080 | -0.26c | +0.00c | 54% | NOISE (no measurable edge) |
| volume_spike | 4862 | -0.26c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1439 | -0.28c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 634 | -0.59c | +0.00c | 48% | NOISE (no measurable edge) |
| cross_platform | 112 | -0.70c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 876 | -0.71c | -0.00c | 53% | NOISE (no measurable edge) |
| price_impact | 285 | -0.77c | -0.50c | 47% | NOISE (no measurable edge) |
| price_jump | 1233 | -0.89c | -1.00c | 47% | NOISE (no measurable edge) |
| thin_market | 44 | -1.97c | -0.30c | 38% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 539 | +0.31c | -0.00c | 51% | NOISE (no measurable edge) |
| politics | 2318 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 377 | -0.32c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2652 | -0.57c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 22 | -1.43c | -0.75c | 37% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 886 | -0.22c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3518 | -0.26c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 836 | -0.47c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 668 | -0.93c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5274 | -0.33c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 634 | -0.59c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 559 | +0.45c | +0.30c | 53% | NOISE (no measurable edge) |
| over a month | 3836 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 990 | -0.45c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 393 | -1.52c | -0.20c | 48% | FADE (signal points the wrong way) |
| under 1 day | 29 | -3.69c | +0.00c | 48% | INSUFFICIENT DATA |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 96 | +0.47c | 41% |
| p_6h (alerted only) | 91 | -0.94c | 43% |
| p_24h (alerted only) | 69 | +0.00c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

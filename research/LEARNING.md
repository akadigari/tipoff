# What the scanner has learned about itself

_Auto-generated 2026-08-16T22:31:52Z. 10000 candidates logged, 5736 with a filled 24h forward price._

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
| alerted (passed gate and score) | 62 | +0.84c | +0.22c | 52% | NOISE (no measurable edge) |
| filtered out | 5459 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 215 | -0.76c | -0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 145 | +1.20c | +0.00c | 53% | FOLLOW |
| thin_market | 75 | +1.05c | +0.30c | 69% | FOLLOW |
| within_trader | 800 | +1.04c | +0.10c | 60% | FOLLOW |
| repeat_actor | 1303 | +0.79c | +0.10c | 59% | NOISE (no measurable edge) |
| large_trade | 1853 | +0.71c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4984 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 526 | +0.07c | -0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 28 | -0.35c | -0.03c | 44% | INSUFFICIENT DATA |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_jump | 873 | -0.67c | -0.40c | 48% | NOISE (no measurable edge) |
| price_impact | 250 | -0.75c | -0.60c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 619 | +0.32c | +0.00c | 53% | NOISE (no measurable edge) |
| politics | 2586 | +0.09c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2383 | +0.04c | -0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 132 | -0.48c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 16 | -2.78c | -0.75c | 40% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 827 | +0.72c | +0.10c | 58% | NOISE (no measurable edge) |
| 70+ | 583 | +0.33c | +0.00c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 794 | +0.13c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3532 | -0.14c | +0.00c | 46% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 526 | +0.07c | -0.00c | 53% | NOISE (no measurable edge) |
| normal | 5210 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 72 | +1.52c | +0.33c | 54% | FOLLOW |
| 3 to 7 days | 428 | +1.04c | +0.20c | 55% | FOLLOW |
| 1 to 4 weeks | 1274 | +0.37c | -0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 356 | +0.37c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3483 | -0.17c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 89 | +0.22c | 52% |
| p_6h (alerted only) | 83 | +0.25c | 45% |
| p_24h (alerted only) | 62 | +0.84c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

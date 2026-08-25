# What the scanner has learned about itself

_Auto-generated 2026-08-25T03:08:10Z. 10000 candidates logged, 5652 with a filled 24h forward price._

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
| filtered out | 5390 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 56 | -0.62c | -0.25c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 206 | -1.08c | +0.00c | 52% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 85 | +0.98c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 291 | +0.76c | -0.10c | 49% | NOISE (no measurable edge) |
| within_trader | 842 | +0.06c | +0.00c | 54% | NOISE (no measurable edge) |
| volume_spike | 4994 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 525 | -0.08c | -0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 758 | -0.31c | +0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 15 | -0.36c | -0.00c | 42% | INSUFFICIENT DATA |
| coordination | 8 | -0.49c | +0.55c | 86% | INSUFFICIENT DATA |
| large_trade | 1846 | -0.52c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1368 | -0.60c | +0.00c | 53% | NOISE (no measurable edge) |
| thin_market | 31 | -3.00c | -0.10c | 47% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1312 | +0.38c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2072 | +0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2178 | -0.39c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 90 | -0.66c | +0.00c | 43% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 730 | +0.24c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3420 | +0.11c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 637 | -0.37c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 865 | -0.67c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5127 | -0.04c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 525 | -0.08c | -0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 37 | +4.93c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 224 | +1.38c | +0.30c | 53% | FOLLOW |
| 1 to 3 days | 262 | +0.29c | +0.53c | 56% | NOISE (no measurable edge) |
| over a month | 3526 | -0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1487 | -0.59c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | +1.13c | 56% |
| p_6h (alerted only) | 83 | +2.50c | 53% |
| p_24h (alerted only) | 56 | -0.62c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

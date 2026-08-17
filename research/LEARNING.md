# What the scanner has learned about itself

_Auto-generated 2026-08-17T01:50:48Z. 10000 candidates logged, 5726 with a filled 24h forward price._

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
| alerted (passed gate and score) | 62 | +0.35c | +0.22c | 52% | NOISE (no measurable edge) |
| filtered out | 5450 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 214 | -0.86c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 142 | +1.23c | +0.00c | 53% | FOLLOW |
| thin_market | 77 | +1.04c | +0.30c | 68% | FOLLOW |
| within_trader | 800 | +0.93c | +0.10c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1302 | +0.71c | +0.10c | 59% | NOISE (no measurable edge) |
| large_trade | 1848 | +0.64c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4978 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 523 | +0.04c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 28 | -0.35c | -0.03c | 44% | INSUFFICIENT DATA |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_jump | 869 | -0.63c | -0.35c | 48% | NOISE (no measurable edge) |
| price_impact | 250 | -0.77c | -0.70c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 618 | +0.26c | +0.00c | 53% | NOISE (no measurable edge) |
| politics | 2568 | +0.11c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2389 | +0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 136 | -1.00c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 15 | -3.40c | -1.00c | 36% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 826 | +0.59c | +0.05c | 57% | NOISE (no measurable edge) |
| 70+ | 581 | +0.34c | -0.00c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 790 | +0.14c | +0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3529 | -0.13c | +0.00c | 46% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5203 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 523 | +0.04c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 73 | +1.52c | +0.40c | 54% | FOLLOW |
| 3 to 7 days | 424 | +0.79c | +0.20c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 361 | +0.43c | +0.10c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1266 | +0.34c | -0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3473 | -0.16c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 90 | +0.34c | 52% |
| p_6h (alerted only) | 84 | +0.17c | 46% |
| p_24h (alerted only) | 62 | +0.35c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

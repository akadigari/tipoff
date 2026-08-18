# What the scanner has learned about itself

_Auto-generated 2026-08-18T11:35:02Z. 10000 candidates logged, 5594 with a filled 24h forward price._

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
| filtered out | 5345 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 49 | +0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 200 | -0.53c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 137 | +1.37c | -0.00c | 51% | FOLLOW |
| within_trader | 785 | +0.86c | +0.10c | 60% | NOISE (no measurable edge) |
| thin_market | 78 | +0.66c | +0.10c | 66% | NOISE (no measurable edge) |
| price_impact | 231 | +0.64c | -0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1270 | +0.50c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1808 | +0.47c | +0.00c | 57% | NOISE (no measurable edge) |
| volume_spike | 4901 | +0.17c | +0.00c | 50% | NOISE (no measurable edge) |
| coordination | 8 | +0.04c | +0.40c | 71% | INSUFFICIENT DATA |
| insiderable | 506 | -0.13c | -0.00c | 52% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.22c | -0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 808 | -0.84c | -0.50c | 47% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 639 | +0.31c | +0.00c | 54% | NOISE (no measurable edge) |
| politics | 2569 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2252 | -0.06c | -0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 120 | -0.67c | +0.00c | 50% | NOISE (no measurable edge) |
| sports | 14 | -3.50c | -0.75c | 38% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 827 | +0.42c | +0.00c | 56% | NOISE (no measurable edge) |
| 70+ | 560 | +0.28c | +0.00c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 754 | +0.02c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3453 | -0.02c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5088 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 506 | -0.13c | -0.00c | 52% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 75 | +1.57c | +0.40c | 55% | FOLLOW |
| 3 to 7 days | 377 | +1.03c | +0.25c | 55% | FOLLOW |
| 1 to 4 weeks | 1238 | +0.39c | +0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3424 | -0.07c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 342 | -0.42c | +0.08c | 53% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 71 | -0.08c | 47% |
| p_6h (alerted only) | 66 | -0.30c | 45% |
| p_24h (alerted only) | 49 | +0.07c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-20T03:05:48Z. 10000 candidates logged, 5193 with a filled 24h forward price._

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
| alerted (passed gate and score) | 38 | -0.21c | +0.00c | 50% | NOISE (no measurable edge) |
| filtered out | 4987 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 168 | -0.90c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 119 | +0.92c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 701 | +0.30c | -0.00c | 55% | NOISE (no measurable edge) |
| coordination | 9 | +0.08c | +0.50c | 75% | INSUFFICIENT DATA |
| volume_spike | 4570 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| thin_market | 47 | -0.20c | +0.05c | 62% | NOISE (no measurable edge) |
| large_trade | 1588 | -0.26c | +0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 26 | -0.34c | +0.02c | 55% | INSUFFICIENT DATA |
| price_impact | 206 | -0.35c | -0.60c | 45% | NOISE (no measurable edge) |
| repeat_actor | 1138 | -0.36c | +0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 475 | -0.51c | -0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 704 | -1.78c | -1.25c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 695 | +0.18c | +0.05c | 55% | NOISE (no measurable edge) |
| politics | 2392 | -0.17c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 1991 | -0.52c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 112 | -1.86c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 3 | -5.50c | -6.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 698 | -0.27c | +0.00c | 50% | NOISE (no measurable edge) |
| under 40 | 3269 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 743 | -0.33c | -0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 483 | -0.37c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4718 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 475 | -0.51c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 58 | +5.19c | +0.00c | 52% | FOLLOW |
| over a month | 3328 | -0.21c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1139 | -0.45c | +0.00c | 48% | NOISE (no measurable edge) |
| 3 to 7 days | 271 | -0.51c | +0.20c | 52% | NOISE (no measurable edge) |
| 1 to 3 days | 265 | -1.18c | -0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 83 | +1.90c | 55% |
| p_6h (alerted only) | 67 | +1.92c | 52% |
| p_24h (alerted only) | 38 | -0.21c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-25T11:37:21Z. 10000 candidates logged, 5596 with a filled 24h forward price._

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
| filtered out | 5335 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 206 | -0.83c | +0.00c | 52% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 55 | -0.99c | -0.50c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 74 | +1.16c | +0.00c | 47% | FOLLOW |
| price_impact | 292 | +0.87c | -0.50c | 48% | NOISE (no measurable edge) |
| within_trader | 833 | -0.01c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4939 | -0.02c | -0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 526 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 762 | -0.22c | -0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 15 | -0.27c | -0.05c | 38% | INSUFFICIENT DATA |
| large_trade | 1829 | -0.52c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1361 | -0.60c | +0.00c | 54% | NOISE (no measurable edge) |
| coordination | 7 | -0.63c | +0.60c | 83% | INSUFFICIENT DATA |
| thin_market | 33 | -2.90c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1318 | +0.30c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2003 | +0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2183 | -0.30c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 92 | -0.86c | -0.25c | 41% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 729 | +0.26c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3377 | +0.11c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 635 | -0.41c | -0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 855 | -0.58c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5070 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 526 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 35 | +5.20c | +0.00c | 45% | FOLLOW |
| 3 to 7 days | 223 | +1.55c | +0.25c | 53% | FOLLOW |
| over a month | 3475 | +0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 244 | -0.01c | +0.50c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1504 | -0.65c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 95 | +1.00c | 55% |
| p_6h (alerted only) | 82 | +2.56c | 52% |
| p_24h (alerted only) | 55 | -0.99c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

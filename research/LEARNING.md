# What the scanner has learned about itself

_Auto-generated 2026-08-20T08:51:39Z. 10000 candidates logged, 5231 with a filled 24h forward price._

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
| alerted (passed gate and score) | 36 | -0.17c | +0.47c | 54% | NOISE (no measurable edge) |
| filtered out | 5031 | -0.22c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 164 | -0.68c | +0.00c | 54% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 8 | +0.84c | +0.55c | 86% | INSUFFICIENT DATA |
| cross_platform | 119 | +0.58c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 698 | +0.35c | +0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4576 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1551 | -0.06c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1110 | -0.13c | +0.05c | 57% | NOISE (no measurable edge) |
| thin_market | 46 | -0.19c | +0.08c | 64% | NOISE (no measurable edge) |
| insiderable | 469 | -0.43c | +0.00c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.45c | +0.05c | 55% | INSUFFICIENT DATA |
| price_impact | 215 | -0.64c | -0.65c | 45% | NOISE (no measurable edge) |
| price_jump | 718 | -1.84c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2443 | -0.02c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 695 | -0.02c | +0.05c | 55% | NOISE (no measurable edge) |
| other | 1979 | -0.47c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 112 | -1.78c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 2 | -5.25c | -5.25c | 50% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 471 | -0.12c | -0.00c | 55% | NOISE (no measurable edge) |
| under 40 | 3343 | -0.21c | +0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 726 | -0.28c | +0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 691 | -0.36c | -0.00c | 49% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4762 | -0.21c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 469 | -0.43c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 57 | +4.63c | +0.00c | 51% | FOLLOW |
| over a month | 3392 | -0.22c | +0.00c | 46% | NOISE (no measurable edge) |
| 3 to 7 days | 265 | -0.30c | +0.20c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1125 | -0.41c | -0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 259 | -1.70c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 80 | +1.89c | 55% |
| p_6h (alerted only) | 66 | +2.68c | 55% |
| p_24h (alerted only) | 36 | -0.17c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

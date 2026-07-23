# What the scanner has learned about itself

_Auto-generated 2026-07-23T10:33:07Z. 10000 candidates logged, 5990 with a filled 24h forward price._

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
| alerted (passed gate and score) | 136 | +0.61c | -0.23c | 46% | NOISE (no measurable edge) |
| filtered out | 5623 | -0.49c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 231 | -1.90c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.31c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 960 | +0.14c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 752 | +0.11c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1741 | +0.00c | +0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4875 | -0.23c | +0.00c | 47% | NOISE (no measurable edge) |
| insiderable | 591 | -0.79c | -0.00c | 44% | NOISE (no measurable edge) |
| price_impact | 355 | -0.82c | -1.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 94 | -1.08c | +0.00c | 45% | FADE (signal points the wrong way) |
| price_jump | 1320 | -2.23c | -1.50c | 44% | FADE (signal points the wrong way) |
| thin_market | 30 | -4.15c | -0.75c | 31% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2712 | -0.28c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2073 | -0.45c | -0.00c | 44% | NOISE (no measurable edge) |
| crypto | 688 | -0.86c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 358 | -1.43c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 159 | -1.96c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 856 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 781 | -0.49c | -0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3803 | -0.51c | -0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 550 | -1.00c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5102 | -0.43c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 591 | -0.79c | -0.00c | 44% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 185 | -0.13c | 39% |
| p_6h (alerted only) | 171 | -1.03c | 45% |
| p_24h (alerted only) | 136 | +0.61c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

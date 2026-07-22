# What the scanner has learned about itself

_Auto-generated 2026-07-22T19:39:43Z. 10000 candidates logged, 5839 with a filled 24h forward price._

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
| alerted (passed gate and score) | 141 | +0.81c | +0.00c | 47% | NOISE (no measurable edge) |
| filtered out | 5478 | -0.51c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 220 | -1.75c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 881 | +0.09c | +0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1662 | -0.02c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 709 | -0.09c | -0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4723 | -0.21c | -0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 11 | -0.33c | -0.30c | 40% | INSUFFICIENT DATA |
| insiderable | 567 | -0.77c | -0.00c | 44% | NOISE (no measurable edge) |
| price_impact | 346 | -0.91c | -1.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 91 | -1.11c | +0.00c | 46% | FADE (signal points the wrong way) |
| price_jump | 1325 | -2.17c | -1.50c | 45% | FADE (signal points the wrong way) |
| thin_market | 27 | -4.09c | -0.50c | 35% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2629 | -0.30c | -0.00c | 49% | NOISE (no measurable edge) |
| politics | 1971 | -0.44c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 678 | -0.89c | -0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 364 | -1.21c | +0.00c | 48% | FADE (signal points the wrong way) |
| sports | 197 | -2.00c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 834 | -0.18c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3740 | -0.52c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 742 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 523 | -1.09c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4805 | -0.45c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 567 | -0.77c | -0.00c | 44% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 198 | +0.01c | 40% |
| p_6h (alerted only) | 183 | -0.77c | 45% |
| p_24h (alerted only) | 141 | +0.81c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

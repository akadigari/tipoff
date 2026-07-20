# What the scanner has learned about itself

_Auto-generated 2026-07-20T22:09:37Z. 8563 candidates logged, 4950 with a filled 24h forward price._

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
| alerted (passed gate and score) | 139 | +0.91c | -0.00c | 48% | NOISE (no measurable edge) |
| filtered out | 4621 | -0.53c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 190 | -1.86c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 693 | +0.11c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 598 | -0.09c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1377 | -0.10c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 3964 | -0.24c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 309 | -0.49c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 477 | -0.83c | +0.00c | 46% | NOISE (no measurable edge) |
| cross_platform | 75 | -0.92c | +0.00c | 46% | NOISE (no measurable edge) |
| fresh_wallet | 9 | -2.07c | -1.00c | 25% | INSUFFICIENT DATA |
| price_jump | 1179 | -2.11c | -1.50c | 44% | FADE (signal points the wrong way) |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 20 | -4.31c | -0.13c | 38% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2212 | -0.31c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 1652 | -0.39c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 554 | -0.70c | -0.08c | 46% | NOISE (no measurable edge) |
| entertainment | 334 | -1.70c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 198 | -1.95c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 717 | -0.17c | -0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 611 | -0.50c | -0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3181 | -0.54c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 441 | -1.16c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 3991 | -0.41c | -0.00c | 47% | NOISE (no measurable edge) |
| high | 477 | -0.83c | +0.00c | 46% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 186 | +0.07c | 42% |
| p_6h (alerted only) | 174 | -0.62c | 47% |
| p_24h (alerted only) | 139 | +0.91c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

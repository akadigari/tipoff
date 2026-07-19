# What the scanner has learned about itself

_Auto-generated 2026-07-19T00:29:28Z. 6927 candidates logged, 4034 with a filled 24h forward price._

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
| alerted (passed gate and score) | 120 | +0.86c | -0.05c | 47% | NOISE (no measurable edge) |
| filtered out | 3763 | -0.40c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 151 | -1.30c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 530 | +0.07c | +0.00c | 53% | NOISE (no measurable edge) |
| within_trader | 458 | +0.05c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1098 | -0.02c | -0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 3263 | -0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 235 | -0.33c | +0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 345 | -0.86c | +0.00c | 46% | NOISE (no measurable edge) |
| cross_platform | 65 | -0.99c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 950 | -1.64c | -1.00c | 46% | FADE (signal points the wrong way) |
| fresh_wallet | 7 | -1.66c | -1.00c | 29% | INSUFFICIENT DATA |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 15 | -5.79c | +0.00c | 36% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 1755 | -0.07c | -0.00c | 49% | NOISE (no measurable edge) |
| politics | 1340 | -0.19c | -0.00c | 46% | NOISE (no measurable edge) |
| crypto | 478 | -0.67c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 269 | -1.84c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 192 | -2.00c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 569 | +0.17c | -0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 2616 | -0.38c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 494 | -0.77c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 355 | -0.85c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 3207 | -0.20c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 345 | -0.86c | +0.00c | 46% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 180 | +0.07c | 42% |
| p_6h (alerted only) | 165 | -0.63c | 46% |
| p_24h (alerted only) | 120 | +0.86c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

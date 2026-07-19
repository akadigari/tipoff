# What the scanner has learned about itself

_Auto-generated 2026-07-19T03:43:05Z. 6982 candidates logged, 4087 with a filled 24h forward price._

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
| alerted (passed gate and score) | 121 | +0.93c | +0.00c | 47% | NOISE (no measurable edge) |
| filtered out | 3813 | -0.39c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 153 | -1.26c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 533 | +0.07c | -0.00c | 53% | NOISE (no measurable edge) |
| within_trader | 460 | +0.04c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1103 | -0.03c | -0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 3301 | -0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 238 | -0.37c | +0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 348 | -0.80c | +0.00c | 46% | NOISE (no measurable edge) |
| cross_platform | 65 | -0.99c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 971 | -1.61c | -1.00c | 47% | FADE (signal points the wrong way) |
| fresh_wallet | 7 | -1.66c | -1.00c | 29% | INSUFFICIENT DATA |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 15 | -5.79c | +0.00c | 36% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 1785 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 1358 | -0.23c | -0.00c | 46% | NOISE (no measurable edge) |
| crypto | 480 | -0.65c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 271 | -1.83c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 193 | -1.94c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 576 | +0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 2654 | -0.37c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 498 | -0.72c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 359 | -0.90c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 3257 | -0.20c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 348 | -0.80c | +0.00c | 46% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 180 | +0.07c | 42% |
| p_6h (alerted only) | 169 | -0.58c | 47% |
| p_24h (alerted only) | 121 | +0.93c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

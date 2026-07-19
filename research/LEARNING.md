# What the scanner has learned about itself

_Auto-generated 2026-07-19T12:04:31Z. 7162 candidates logged, 4185 with a filled 24h forward price._

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
| alerted (passed gate and score) | 127 | +0.91c | -0.00c | 48% | NOISE (no measurable edge) |
| filtered out | 3901 | -0.43c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 157 | -1.36c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 553 | +0.06c | -0.00c | 53% | NOISE (no measurable edge) |
| within_trader | 477 | +0.01c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1131 | -0.02c | +0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 3362 | -0.18c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 251 | -0.27c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 364 | -0.64c | +0.00c | 48% | NOISE (no measurable edge) |
| cross_platform | 65 | -0.99c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1004 | -1.77c | -1.00c | 46% | FADE (signal points the wrong way) |
| fresh_wallet | 8 | -2.33c | -1.50c | 25% | INSUFFICIENT DATA |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 17 | -4.97c | +0.00c | 38% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 1842 | -0.18c | -0.00c | 49% | NOISE (no measurable edge) |
| politics | 1383 | -0.21c | +0.00c | 46% | NOISE (no measurable edge) |
| crypto | 488 | -0.64c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 278 | -1.66c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 194 | -1.91c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 589 | +0.10c | -0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 2716 | -0.41c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 510 | -0.66c | +0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 370 | -1.01c | +0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 3339 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 364 | -0.64c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 181 | +0.05c | 41% |
| p_6h (alerted only) | 169 | -0.58c | 47% |
| p_24h (alerted only) | 127 | +0.91c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

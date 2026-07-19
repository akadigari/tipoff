# What the scanner has learned about itself

_Auto-generated 2026-07-19T21:03:05Z. 7678 candidates logged, 4400 with a filled 24h forward price._

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
| alerted (passed gate and score) | 134 | +0.77c | +0.00c | 48% | NOISE (no measurable edge) |
| filtered out | 4101 | -0.45c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 165 | -1.41c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 588 | -0.09c | -0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1197 | -0.12c | -0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 271 | -0.14c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 3518 | -0.22c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 503 | -0.26c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 402 | -0.66c | +0.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 70 | -1.32c | +0.00c | 44% | FADE (signal points the wrong way) |
| price_jump | 1076 | -1.78c | -1.00c | 45% | FADE (signal points the wrong way) |
| fresh_wallet | 9 | -2.07c | -1.00c | 25% | INSUFFICIENT DATA |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 18 | -4.72c | -0.13c | 36% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 1959 | -0.16c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 1445 | -0.25c | -0.00c | 46% | NOISE (no measurable edge) |
| crypto | 509 | -0.67c | -0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 291 | -1.94c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 196 | -1.96c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 633 | +0.06c | -0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 2837 | -0.39c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 540 | -0.90c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 390 | -1.03c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 3516 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 402 | -0.66c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 185 | +0.07c | 42% |
| p_6h (alerted only) | 170 | -0.72c | 47% |
| p_24h (alerted only) | 134 | +0.77c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

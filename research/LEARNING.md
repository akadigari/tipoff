# What the scanner has learned about itself

_Auto-generated 2026-07-19T19:20:05Z. 7557 candidates logged, 4354 with a filled 24h forward price._

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
| alerted (passed gate and score) | 133 | +0.90c | -0.00c | 48% | NOISE (no measurable edge) |
| filtered out | 4058 | -0.48c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 163 | -1.36c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 582 | -0.04c | +0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1186 | -0.09c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 269 | -0.18c | -0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 501 | -0.22c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 3479 | -0.23c | +0.00c | 48% | NOISE (no measurable edge) |
| insiderable | 396 | -0.62c | +0.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 69 | -1.33c | +0.00c | 44% | FADE (signal points the wrong way) |
| price_jump | 1069 | -1.81c | -1.00c | 45% | FADE (signal points the wrong way) |
| fresh_wallet | 9 | -2.07c | -1.00c | 25% | INSUFFICIENT DATA |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 17 | -4.97c | +0.00c | 38% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 1941 | -0.23c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 1425 | -0.24c | +0.00c | 46% | NOISE (no measurable edge) |
| crypto | 503 | -0.63c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 289 | -1.94c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 196 | -1.96c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 625 | +0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 2806 | -0.45c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 534 | -0.86c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 389 | -0.99c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 3476 | -0.34c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 396 | -0.62c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 184 | +0.05c | 42% |
| p_6h (alerted only) | 170 | -0.72c | 47% |
| p_24h (alerted only) | 133 | +0.90c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

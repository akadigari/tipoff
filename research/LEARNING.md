# What the scanner has learned about itself

_Auto-generated 2026-07-19T09:59:35Z. 7110 candidates logged, 4158 with a filled 24h forward price._

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
| alerted (passed gate and score) | 126 | +0.91c | +0.00c | 48% | NOISE (no measurable edge) |
| filtered out | 3875 | -0.41c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 157 | -1.36c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 545 | +0.06c | -0.00c | 53% | NOISE (no measurable edge) |
| within_trader | 473 | -0.00c | -0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1122 | -0.02c | -0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 3345 | -0.18c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 246 | -0.19c | +0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 359 | -0.68c | +0.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 65 | -0.99c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 995 | -1.71c | -1.00c | 46% | FADE (signal points the wrong way) |
| fresh_wallet | 8 | -2.33c | -1.50c | 25% | INSUFFICIENT DATA |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 17 | -4.97c | +0.00c | 38% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 1824 | -0.14c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 1377 | -0.21c | +0.00c | 46% | NOISE (no measurable edge) |
| crypto | 486 | -0.65c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 278 | -1.66c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 193 | -1.94c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 586 | +0.09c | -0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 2699 | -0.39c | -0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 506 | -0.68c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 367 | -0.98c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 3317 | -0.25c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 359 | -0.68c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 181 | +0.05c | 41% |
| p_6h (alerted only) | 169 | -0.58c | 47% |
| p_24h (alerted only) | 126 | +0.91c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

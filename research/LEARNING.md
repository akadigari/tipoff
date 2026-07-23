# What the scanner has learned about itself

_Auto-generated 2026-07-23T23:07:01Z. 10000 candidates logged, 5997 with a filled 24h forward price._

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
| alerted (passed gate and score) | 127 | +0.22c | -0.50c | 44% | NOISE (no measurable edge) |
| filtered out | 5633 | -0.39c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 237 | -1.86c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.31c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1026 | +0.00c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 781 | -0.01c | -0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1806 | -0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4874 | -0.26c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 356 | -0.42c | -0.75c | 48% | NOISE (no measurable edge) |
| insiderable | 622 | -0.73c | +0.00c | 45% | NOISE (no measurable edge) |
| cross_platform | 86 | -1.58c | +0.00c | 44% | FADE (signal points the wrong way) |
| price_jump | 1333 | -1.83c | -1.00c | 45% | FADE (signal points the wrong way) |
| thin_market | 31 | -4.02c | -0.50c | 31% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 90 | -0.03c | -0.00c | 54% | NOISE (no measurable edge) |
| other | 2776 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2110 | -0.44c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 678 | -0.69c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 343 | -1.36c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 875 | -0.24c | -0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3744 | -0.36c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 803 | -0.51c | -0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 575 | -1.13c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5351 | -0.41c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 622 | -0.73c | +0.00c | 45% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 178 | -0.02c | 43% |
| p_6h (alerted only) | 160 | -1.24c | 45% |
| p_24h (alerted only) | 127 | +0.22c | 44% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

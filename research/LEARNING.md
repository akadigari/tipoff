# What the scanner has learned about itself

_Auto-generated 2026-07-24T15:03:08Z. 10000 candidates logged, 5906 with a filled 24h forward price._

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
| alerted (passed gate and score) | 105 | +0.35c | -0.30c | 45% | NOISE (no measurable edge) |
| filtered out | 5565 | -0.42c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 236 | -1.92c | +0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 13 | +2.82c | -1.00c | 42% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1054 | +0.05c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1808 | -0.09c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 787 | -0.11c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4773 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 357 | -0.39c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 604 | -0.77c | -0.00c | 45% | NOISE (no measurable edge) |
| price_jump | 1324 | -1.81c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 85 | -2.09c | +0.00c | 43% | FADE (signal points the wrong way) |
| thin_market | 30 | -3.47c | -0.50c | 32% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 64 | +0.47c | +0.28c | 57% | NOISE (no measurable edge) |
| crypto | 677 | -0.34c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2761 | -0.40c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2069 | -0.49c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 335 | -1.25c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 866 | -0.34c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3668 | -0.40c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 803 | -0.50c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 569 | -1.05c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5302 | -0.43c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 604 | -0.77c | -0.00c | 45% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 151 | -0.88c | 41% |
| p_6h (alerted only) | 141 | -1.50c | 44% |
| p_24h (alerted only) | 105 | +0.35c | 45% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

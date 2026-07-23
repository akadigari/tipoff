# What the scanner has learned about itself

_Auto-generated 2026-07-23T03:37:59Z. 10000 candidates logged, 5975 with a filled 24h forward price._

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
| alerted (passed gate and score) | 137 | +0.61c | -0.30c | 45% | NOISE (no measurable edge) |
| filtered out | 5611 | -0.53c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 227 | -1.95c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.49c | -0.15c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 938 | +0.08c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 739 | +0.03c | -0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1722 | -0.02c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4865 | -0.23c | +0.00c | 47% | NOISE (no measurable edge) |
| insiderable | 585 | -0.76c | +0.00c | 45% | NOISE (no measurable edge) |
| price_impact | 349 | -0.90c | -1.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 95 | -1.09c | +0.00c | 45% | FADE (signal points the wrong way) |
| price_jump | 1324 | -2.30c | -1.50c | 44% | FADE (signal points the wrong way) |
| thin_market | 29 | -4.28c | -1.00c | 32% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2701 | -0.33c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2058 | -0.45c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 682 | -0.92c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 361 | -1.41c | -0.00c | 47% | FADE (signal points the wrong way) |
| sports | 173 | -2.16c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 856 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3808 | -0.56c | -0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 766 | -0.57c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 545 | -0.97c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5030 | -0.47c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 585 | -0.76c | +0.00c | 45% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 190 | +0.06c | 40% |
| p_6h (alerted only) | 177 | -0.77c | 45% |
| p_24h (alerted only) | 137 | +0.61c | 45% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-07-22T17:36:17Z. 9910 candidates logged, 5797 with a filled 24h forward price._

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
| alerted (passed gate and score) | 141 | +0.81c | +0.00c | 47% | NOISE (no measurable edge) |
| filtered out | 5437 | -0.54c | -0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 219 | -1.76c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 871 | +0.06c | -0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1646 | -0.03c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 702 | -0.10c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4680 | -0.22c | +0.00c | 47% | NOISE (no measurable edge) |
| insiderable | 562 | -0.77c | +0.00c | 45% | NOISE (no measurable edge) |
| price_impact | 345 | -0.87c | -1.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 91 | -1.11c | +0.00c | 46% | FADE (signal points the wrong way) |
| fresh_wallet | 10 | -1.46c | -0.65c | 33% | INSUFFICIENT DATA |
| price_jump | 1327 | -2.27c | -1.50c | 45% | FADE (signal points the wrong way) |
| thin_market | 27 | -4.09c | -0.50c | 35% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2607 | -0.29c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 1947 | -0.45c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 675 | -1.03c | -0.00c | 47% | FADE (signal points the wrong way) |
| entertainment | 369 | -1.42c | +0.00c | 48% | FADE (signal points the wrong way) |
| sports | 199 | -1.95c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 827 | -0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3715 | -0.55c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 735 | -0.61c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 520 | -1.12c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4753 | -0.45c | -0.00c | 47% | NOISE (no measurable edge) |
| high | 562 | -0.77c | +0.00c | 45% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 197 | +0.01c | 40% |
| p_6h (alerted only) | 182 | -0.72c | 46% |
| p_24h (alerted only) | 141 | +0.81c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

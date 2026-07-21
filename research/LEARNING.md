# What the scanner has learned about itself

_Auto-generated 2026-07-21T19:45:47Z. 9193 candidates logged, 5407 with a filled 24h forward price._

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
| alerted (passed gate and score) | 139 | +0.91c | -0.00c | 48% | NOISE (no measurable edge) |
| filtered out | 5065 | -0.56c | -0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 203 | -1.92c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| repeat_actor | 792 | +0.00c | -0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1527 | -0.08c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 651 | -0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4358 | -0.24c | -0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 334 | -0.69c | -0.75c | 48% | NOISE (no measurable edge) |
| insiderable | 522 | -0.80c | +0.00c | 45% | NOISE (no measurable edge) |
| cross_platform | 83 | -1.21c | +0.00c | 43% | FADE (signal points the wrong way) |
| fresh_wallet | 9 | -2.07c | -1.00c | 25% | INSUFFICIENT DATA |
| price_jump | 1254 | -2.28c | -1.50c | 45% | FADE (signal points the wrong way) |
| chatter | 3 | -2.63c | -2.20c | 0% | INSUFFICIENT DATA |
| thin_market | 22 | -3.95c | -0.13c | 39% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 1796 | -0.36c | +0.00c | 44% | NOISE (no measurable edge) |
| other | 2438 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| crypto | 618 | -0.98c | -0.05c | 47% | NOISE (no measurable edge) |
| entertainment | 357 | -1.50c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 198 | -1.95c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 776 | -0.20c | -0.00c | 47% | NOISE (no measurable edge) |
| under 40 | 3464 | -0.56c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 686 | -0.58c | -0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 481 | -1.18c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4403 | -0.46c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 522 | -0.80c | +0.00c | 45% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 191 | +0.04c | 41% |
| p_6h (alerted only) | 177 | -0.69c | 46% |
| p_24h (alerted only) | 139 | +0.91c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

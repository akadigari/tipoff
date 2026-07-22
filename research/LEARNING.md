# What the scanner has learned about itself

_Auto-generated 2026-07-22T10:33:14Z. 9594 candidates logged, 5675 with a filled 24h forward price._

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
| filtered out | 5320 | -0.57c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 214 | -1.85c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 844 | -0.00c | -0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1607 | -0.07c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 692 | -0.15c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4584 | -0.24c | +0.00c | 47% | NOISE (no measurable edge) |
| insiderable | 555 | -0.78c | +0.00c | 45% | NOISE (no measurable edge) |
| price_impact | 344 | -0.83c | -1.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 90 | -1.09c | +0.00c | 46% | FADE (signal points the wrong way) |
| fresh_wallet | 10 | -1.46c | -0.65c | 33% | INSUFFICIENT DATA |
| price_jump | 1297 | -2.34c | -1.50c | 44% | FADE (signal points the wrong way) |
| thin_market | 26 | -4.27c | -0.75c | 32% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2542 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 1914 | -0.44c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 652 | -0.95c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 368 | -1.42c | +0.00c | 48% | FADE (signal points the wrong way) |
| sports | 199 | -1.95c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 812 | -0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3635 | -0.58c | -0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 721 | -0.62c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 507 | -1.21c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4638 | -0.48c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 555 | -0.78c | +0.00c | 45% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 193 | +0.10c | 41% |
| p_6h (alerted only) | 179 | -0.70c | 46% |
| p_24h (alerted only) | 141 | +0.81c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

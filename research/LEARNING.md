# What the scanner has learned about itself

_Auto-generated 2026-07-23T21:17:29Z. 10000 candidates logged, 5990 with a filled 24h forward price._

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
| alerted (passed gate and score) | 128 | +0.33c | -0.47c | 45% | NOISE (no measurable edge) |
| filtered out | 5626 | -0.38c | +0.00c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 236 | -1.90c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.31c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1019 | +0.03c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 776 | -0.00c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1792 | -0.05c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4871 | -0.25c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 356 | -0.40c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 616 | -0.71c | +0.00c | 45% | NOISE (no measurable edge) |
| cross_platform | 86 | -1.58c | +0.00c | 44% | FADE (signal points the wrong way) |
| price_jump | 1329 | -1.83c | -1.00c | 45% | FADE (signal points the wrong way) |
| thin_market | 30 | -4.15c | -0.75c | 31% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 100 | +0.04c | -0.00c | 54% | NOISE (no measurable edge) |
| other | 2766 | -0.26c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2102 | -0.42c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 676 | -0.68c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 346 | -1.35c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 870 | -0.21c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3749 | -0.35c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 800 | -0.46c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 571 | -1.16c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5317 | -0.41c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 616 | -0.71c | +0.00c | 45% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 180 | -0.06c | 43% |
| p_6h (alerted only) | 161 | -1.25c | 45% |
| p_24h (alerted only) | 128 | +0.33c | 45% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

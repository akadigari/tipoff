# What the scanner has learned about itself

_Auto-generated 2026-07-25T12:07:22Z. 10000 candidates logged, 5917 with a filled 24h forward price._

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
| filtered out | 5591 | -0.52c | -0.00c | 47% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 99 | -1.74c | -1.00c | 40% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 227 | -1.91c | -0.00c | 42% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| within_trader | 772 | -0.19c | +0.00c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1089 | -0.20c | -0.00c | 50% | NOISE (no measurable edge) |
| large_trade | 1797 | -0.30c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4793 | -0.37c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 346 | -0.93c | -0.50c | 47% | NOISE (no measurable edge) |
| insiderable | 606 | -1.06c | +0.00c | 46% | FADE (signal points the wrong way) |
| price_jump | 1324 | -2.06c | -1.05c | 45% | FADE (signal points the wrong way) |
| cross_platform | 88 | -2.07c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 28 | -3.77c | -0.75c | 29% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 60 | +0.58c | +0.40c | 59% | NOISE (no measurable edge) |
| politics | 2083 | -0.54c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 665 | -0.56c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2775 | -0.62c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 334 | -1.07c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3681 | -0.47c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 873 | -0.67c | -0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 792 | -0.76c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 571 | -1.11c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5311 | -0.54c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 606 | -1.06c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +3.64c | +1.02c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 234 | +0.71c | +0.75c | 56% | NOISE (no measurable edge) |
| over a month | 3527 | -0.49c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 3 days | 207 | -0.59c | -0.45c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1842 | -1.06c | +0.00c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 138 | -0.79c | 45% |
| p_6h (alerted only) | 130 | -1.25c | 47% |
| p_24h (alerted only) | 99 | -1.74c | 40% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-07-25T00:12:43Z. 10000 candidates logged, 5948 with a filled 24h forward price._

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
| filtered out | 5613 | -0.46c | -0.00c | 47% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 102 | -1.09c | -0.58c | 41% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 233 | -1.96c | +0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1077 | -0.07c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 779 | -0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| large_trade | 1801 | -0.25c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4829 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 347 | -0.45c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 612 | -1.03c | +0.00c | 45% | FADE (signal points the wrong way) |
| price_jump | 1322 | -1.99c | -1.30c | 44% | FADE (signal points the wrong way) |
| cross_platform | 88 | -2.07c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 30 | -3.47c | -0.50c | 32% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 61 | +0.56c | +0.30c | 58% | NOISE (no measurable edge) |
| crypto | 666 | -0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2092 | -0.52c | +0.00c | 44% | NOISE (no measurable edge) |
| other | 2802 | -0.55c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 327 | -1.18c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3695 | -0.40c | -0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 880 | -0.52c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 806 | -0.75c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 567 | -1.05c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5336 | -0.47c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 612 | -1.03c | +0.00c | 45% | FADE (signal points the wrong way) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 20 | +3.40c | +1.02c | 58% | INSUFFICIENT DATA |
| 3 to 7 days | 235 | +0.66c | +0.75c | 56% | NOISE (no measurable edge) |
| over a month | 3528 | -0.50c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 3 days | 205 | -0.61c | -0.45c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1869 | -0.83c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 143 | -0.78c | 45% |
| p_6h (alerted only) | 134 | -1.41c | 46% |
| p_24h (alerted only) | 102 | -1.09c | 41% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

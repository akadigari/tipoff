# What the scanner has learned about itself

_Auto-generated 2026-07-28T17:43:30Z. 10000 candidates logged, 5801 with a filled 24h forward price._

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
| filtered out | 5491 | -0.41c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 79 | -1.18c | -1.00c | 42% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 231 | -1.65c | -0.00c | 41% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 17 | +1.38c | -0.10c | 44% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1231 | +0.05c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1884 | -0.04c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 820 | -0.12c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4664 | -0.31c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 349 | -0.66c | -0.50c | 47% | NOISE (no measurable edge) |
| insiderable | 662 | -0.96c | +0.00c | 47% | NOISE (no measurable edge) |
| thin_market | 31 | -1.33c | -0.50c | 41% | FADE (signal points the wrong way) |
| price_jump | 1306 | -1.78c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 88 | -3.00c | -0.10c | 39% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 589 | -0.13c | -0.00c | 52% | NOISE (no measurable edge) |
| other | 2673 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2108 | -0.54c | +0.00c | 44% | NOISE (no measurable edge) |
| sports | 40 | -0.55c | -0.00c | 53% | NOISE (no measurable edge) |
| entertainment | 391 | -1.30c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 842 | -0.21c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3511 | -0.31c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 862 | -0.94c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 586 | -1.09c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5139 | -0.40c | -0.00c | 47% | NOISE (no measurable edge) |
| high | 662 | -0.96c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 20 | +9.76c | +5.52c | 60% | INSUFFICIENT DATA |
| 3 to 7 days | 400 | +0.51c | +0.42c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 245 | +0.50c | +0.40c | 53% | NOISE (no measurable edge) |
| over a month | 3476 | -0.46c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1557 | -1.05c | -0.05c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 108 | +0.01c | 47% |
| p_6h (alerted only) | 100 | -0.57c | 48% |
| p_24h (alerted only) | 79 | -1.18c | 42% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

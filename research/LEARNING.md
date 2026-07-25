# What the scanner has learned about itself

_Auto-generated 2026-07-25T16:10:35Z. 10000 candidates logged, 5913 with a filled 24h forward price._

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
| filtered out | 5590 | -0.52c | +0.00c | 47% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 100 | -1.81c | -1.03c | 40% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 223 | -1.93c | -0.00c | 42% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1098 | -0.18c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 773 | -0.21c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1804 | -0.28c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4772 | -0.36c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 345 | -0.91c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 608 | -1.08c | +0.00c | 46% | FADE (signal points the wrong way) |
| price_jump | 1361 | -2.01c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 90 | -2.04c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 26 | -3.54c | -0.50c | 35% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 60 | +0.58c | +0.40c | 59% | NOISE (no measurable edge) |
| politics | 2067 | -0.54c | +0.00c | 44% | NOISE (no measurable edge) |
| other | 2793 | -0.56c | -0.00c | 48% | NOISE (no measurable edge) |
| crypto | 654 | -0.66c | -0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 339 | -1.26c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3660 | -0.46c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 877 | -0.69c | -0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 794 | -0.70c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 582 | -1.10c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5305 | -0.53c | -0.00c | 47% | NOISE (no measurable edge) |
| high | 608 | -1.08c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +3.64c | +1.02c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 235 | +0.76c | +0.75c | 57% | NOISE (no measurable edge) |
| over a month | 3530 | -0.50c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 3 days | 211 | -0.61c | -0.45c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1831 | -1.03c | +0.00c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 136 | -0.89c | 44% |
| p_6h (alerted only) | 128 | -1.32c | 46% |
| p_24h (alerted only) | 100 | -1.81c | 40% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

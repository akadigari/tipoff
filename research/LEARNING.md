# What the scanner has learned about itself

_Auto-generated 2026-07-26T10:09:06Z. 10000 candidates logged, 5944 with a filled 24h forward price._

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
| filtered out | 5623 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 93 | -1.29c | -1.00c | 41% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 228 | -1.84c | +0.00c | 44% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 13 | +3.21c | -1.00c | 42% | INSUFFICIENT DATA |
| coordination | 5 | +2.02c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1141 | -0.07c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1830 | -0.20c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 783 | -0.26c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4765 | -0.28c | -0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 354 | -0.46c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 634 | -0.84c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1393 | -1.58c | -1.00c | 46% | FADE (signal points the wrong way) |
| cross_platform | 95 | -1.93c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 26 | -2.09c | -0.75c | 35% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 61 | +0.53c | +0.25c | 58% | NOISE (no measurable edge) |
| crypto | 626 | +0.14c | +0.00c | 52% | NOISE (no measurable edge) |
| other | 2799 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2104 | -0.51c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 354 | -0.93c | +0.00c | 49% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3664 | -0.30c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 800 | -0.39c | +0.00c | 49% | NOISE (no measurable edge) |
| 40 to 54 | 888 | -0.58c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 592 | -1.19c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5310 | -0.39c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 634 | -0.84c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 19 | +3.18c | -0.50c | 47% | INSUFFICIENT DATA |
| 3 to 7 days | 271 | +1.04c | +0.80c | 58% | FOLLOW |
| 1 to 3 days | 223 | +0.25c | +0.25c | 51% | NOISE (no measurable edge) |
| over a month | 3555 | -0.49c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1787 | -0.70c | -0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 127 | -0.47c | 46% |
| p_6h (alerted only) | 120 | -1.15c | 46% |
| p_24h (alerted only) | 93 | -1.29c | 41% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

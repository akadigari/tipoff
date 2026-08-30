# What the scanner has learned about itself

_Auto-generated 2026-08-30T23:25:20Z. 10000 candidates logged, 6544 with a filled 24h forward price._

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
| alerted (passed gate and score) | 68 | +1.89c | +0.00c | 51% | FOLLOW |
| filtered out | 6238 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 238 | -1.13c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 76 | +1.01c | +0.00c | 42% | FOLLOW |
| fresh_wallet | 24 | +0.39c | +0.00c | 45% | INSUFFICIENT DATA |
| price_impact | 347 | +0.21c | -0.85c | 48% | NOISE (no measurable edge) |
| insiderable | 578 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 5750 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 951 | -0.16c | +0.00c | 55% | NOISE (no measurable edge) |
| large_trade | 2209 | -0.37c | +0.00c | 53% | NOISE (no measurable edge) |
| repeat_actor | 1609 | -0.53c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 934 | -0.94c | -0.62c | 48% | NOISE (no measurable edge) |
| coordination | 7 | -1.34c | -0.20c | 43% | INSUFFICIENT DATA |
| thin_market | 40 | -2.28c | +0.08c | 58% | FADE (signal points the wrong way) |
| chatter | 6 | -3.58c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2330 | -0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2553 | -0.11c | +0.00c | 48% | NOISE (no measurable edge) |
| crypto | 1549 | -0.19c | -0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 112 | -1.79c | -0.75c | 38% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3909 | +0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| 40 to 54 | 855 | +0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 1029 | -0.51c | +0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 751 | -0.73c | -0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 578 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| normal | 5966 | -0.14c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 16 | +7.88c | +19.30c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 563 | +0.65c | +0.30c | 55% | NOISE (no measurable edge) |
| over a month | 4098 | -0.04c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 296 | -0.51c | +0.53c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1474 | -0.72c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 99 | +1.13c | 55% |
| p_6h (alerted only) | 90 | +2.86c | 55% |
| p_24h (alerted only) | 68 | +1.89c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

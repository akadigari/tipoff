# What the scanner has learned about itself

_Auto-generated 2026-08-28T20:10:29Z. 10000 candidates logged, 6558 with a filled 24h forward price._

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
| alerted (passed gate and score) | 67 | +1.38c | +0.00c | 48% | FOLLOW |
| filtered out | 6260 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 231 | -1.18c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 65 | +1.20c | +0.00c | 47% | FOLLOW |
| price_impact | 348 | +0.07c | -0.93c | 47% | NOISE (no measurable edge) |
| insiderable | 583 | +0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| volume_spike | 5762 | -0.06c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 947 | -0.22c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 20 | -0.32c | -0.03c | 38% | INSUFFICIENT DATA |
| large_trade | 2194 | -0.41c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1612 | -0.55c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 943 | -0.94c | -0.50c | 49% | NOISE (no measurable edge) |
| coordination | 7 | -1.34c | -0.20c | 43% | INSUFFICIENT DATA |
| thin_market | 32 | -3.13c | +0.08c | 55% | FADE (signal points the wrong way) |
| chatter | 6 | -3.58c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2302 | -0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 1583 | -0.06c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2568 | -0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 105 | -1.57c | -1.00c | 35% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 848 | +0.13c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3934 | +0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 1036 | -0.54c | +0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 740 | -0.83c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 583 | +0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| normal | 5975 | -0.12c | -0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 563 | +0.57c | +0.30c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 285 | +0.25c | +0.95c | 53% | NOISE (no measurable edge) |
| over a month | 4058 | -0.07c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1532 | -0.72c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 99 | +1.22c | 54% |
| p_6h (alerted only) | 89 | +2.97c | 54% |
| p_24h (alerted only) | 67 | +1.38c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-15T19:28:57Z. 10000 candidates logged, 5642 with a filled 24h forward price._

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
| alerted (passed gate and score) | 66 | +1.02c | +0.50c | 51% | FOLLOW |
| filtered out | 5367 | +0.16c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 209 | -1.04c | -0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 65 | +1.70c | +0.50c | 69% | FOLLOW |
| cross_platform | 157 | +1.07c | +0.00c | 50% | FOLLOW |
| within_trader | 743 | +1.02c | +0.10c | 60% | FOLLOW |
| repeat_actor | 1260 | +0.90c | +0.15c | 59% | NOISE (no measurable edge) |
| large_trade | 1810 | +0.79c | +0.10c | 58% | NOISE (no measurable edge) |
| volume_spike | 4871 | +0.24c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 489 | +0.10c | -0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 891 | -0.28c | -0.00c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 24 | -0.43c | -0.08c | 41% | INSUFFICIENT DATA |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 251 | -0.74c | -0.55c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 598 | +0.31c | +0.00c | 53% | NOISE (no measurable edge) |
| entertainment | 125 | +0.22c | -0.50c | 43% | NOISE (no measurable edge) |
| other | 2369 | +0.16c | -0.00c | 50% | NOISE (no measurable edge) |
| politics | 2532 | +0.08c | +0.00c | 50% | NOISE (no measurable edge) |
| sports | 18 | -4.58c | -1.50c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 797 | +0.87c | +0.05c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 801 | +0.31c | -0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 553 | +0.28c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3491 | -0.11c | -0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5153 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 489 | +0.10c | -0.00c | 54% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 61 | +1.85c | +0.40c | 54% | FOLLOW |
| 3 to 7 days | 418 | +1.34c | +0.25c | 56% | FOLLOW |
| 1 to 3 days | 337 | +0.74c | +0.30c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1265 | +0.48c | +0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3456 | -0.17c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | -0.05c | 48% |
| p_6h (alerted only) | 87 | +0.02c | 44% |
| p_24h (alerted only) | 66 | +1.02c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

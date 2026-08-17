# What the scanner has learned about itself

_Auto-generated 2026-08-17T07:11:15Z. 10000 candidates logged, 5753 with a filled 24h forward price._

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
| alerted (passed gate and score) | 59 | +0.14c | +0.00c | 49% | NOISE (no measurable edge) |
| filtered out | 5482 | +0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 212 | -0.84c | +0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 137 | +1.19c | +0.00c | 52% | FOLLOW |
| thin_market | 83 | +1.00c | +0.30c | 68% | FOLLOW |
| within_trader | 793 | +0.88c | +0.10c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1298 | +0.72c | +0.10c | 60% | NOISE (no measurable edge) |
| large_trade | 1840 | +0.62c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 5006 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 249 | +0.07c | -0.45c | 48% | NOISE (no measurable edge) |
| insiderable | 535 | +0.02c | +0.00c | 52% | NOISE (no measurable edge) |
| fresh_wallet | 29 | -0.42c | -0.05c | 42% | INSUFFICIENT DATA |
| price_jump | 874 | -0.45c | -0.00c | 49% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 616 | +0.29c | +0.00c | 53% | NOISE (no measurable edge) |
| politics | 2579 | +0.15c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2409 | +0.09c | -0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 134 | -1.15c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 15 | -3.40c | -1.00c | 36% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 828 | +0.50c | +0.05c | 57% | NOISE (no measurable edge) |
| 70+ | 580 | +0.31c | -0.00c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 787 | +0.20c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3558 | -0.05c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5218 | +0.11c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 535 | +0.02c | +0.00c | 52% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 75 | +1.22c | +0.25c | 53% | FOLLOW |
| 3 to 7 days | 419 | +0.79c | +0.20c | 56% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1268 | +0.53c | +0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3491 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 364 | -0.14c | +0.05c | 53% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 87 | +0.25c | 51% |
| p_6h (alerted only) | 81 | +0.38c | 48% |
| p_24h (alerted only) | 59 | +0.14c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

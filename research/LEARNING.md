# What the scanner has learned about itself

_Auto-generated 2026-08-16T15:31:20Z. 10000 candidates logged, 5771 with a filled 24h forward price._

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
| alerted (passed gate and score) | 66 | +0.75c | +0.22c | 52% | NOISE (no measurable edge) |
| filtered out | 5488 | +0.14c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 217 | -0.83c | -0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 148 | +1.15c | +0.00c | 53% | FOLLOW |
| thin_market | 70 | +1.09c | +0.40c | 68% | FOLLOW |
| within_trader | 798 | +0.97c | +0.10c | 59% | NOISE (no measurable edge) |
| repeat_actor | 1305 | +0.74c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1860 | +0.68c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4999 | +0.22c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 518 | +0.04c | -0.00c | 53% | NOISE (no measurable edge) |
| price_impact | 257 | -0.45c | -0.50c | 47% | NOISE (no measurable edge) |
| price_jump | 892 | -0.50c | +0.00c | 48% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| fresh_wallet | 29 | -1.00c | -0.05c | 42% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 621 | +0.33c | -0.00c | 54% | NOISE (no measurable edge) |
| entertainment | 129 | +0.20c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2405 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2598 | +0.07c | +0.00c | 51% | NOISE (no measurable edge) |
| sports | 18 | -4.58c | -1.50c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 828 | +0.76c | +0.10c | 58% | NOISE (no measurable edge) |
| 70+ | 586 | +0.23c | -0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 795 | +0.19c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3562 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5253 | +0.11c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 518 | +0.04c | -0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 69 | +1.64c | +0.95c | 55% | FOLLOW |
| 3 to 7 days | 430 | +1.24c | +0.23c | 56% | FOLLOW |
| 1 to 3 days | 343 | +0.54c | +0.15c | 56% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1289 | +0.45c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3518 | -0.18c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +0.02c | 49% |
| p_6h (alerted only) | 88 | +0.15c | 45% |
| p_24h (alerted only) | 66 | +0.75c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

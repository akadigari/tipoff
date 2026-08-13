# What the scanner has learned about itself

_Auto-generated 2026-08-13T16:05:40Z. 10000 candidates logged, 5697 with a filled 24h forward price._

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
| filtered out | 5384 | +0.16c | +0.00c | 50% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 81 | -0.11c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 232 | -0.84c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 160 | +1.54c | +0.00c | 55% | FOLLOW |
| thin_market | 69 | +1.29c | +0.45c | 66% | FOLLOW |
| repeat_actor | 1376 | +0.72c | +0.15c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 24 | +0.54c | -0.08c | 38% | INSUFFICIENT DATA |
| large_trade | 1951 | +0.54c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 826 | +0.51c | +0.10c | 58% | NOISE (no measurable edge) |
| volume_spike | 4907 | +0.22c | +0.00c | 51% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| price_jump | 903 | -0.02c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 508 | -0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 256 | -0.36c | -0.50c | 47% | NOISE (no measurable edge) |
| coordination | 4 | -1.60c | -0.70c | 33% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2380 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2594 | +0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 556 | -0.03c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 141 | -1.06c | +0.00c | 45% | FADE (signal points the wrong way) |
| sports | 26 | -4.88c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 854 | +0.48c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 811 | +0.39c | -0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 598 | +0.37c | +0.00c | 57% | NOISE (no measurable edge) |
| under 40 | 3434 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5189 | +0.15c | -0.00c | 50% | NOISE (no measurable edge) |
| high | 508 | -0.19c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 388 | +1.46c | +0.40c | 58% | FOLLOW |
| 1 to 4 weeks | 1351 | +0.45c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3437 | -0.05c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 351 | -0.24c | +0.10c | 53% | NOISE (no measurable edge) |
| under 1 day | 67 | -1.19c | +0.95c | 55% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.31c | 47% |
| p_6h (alerted only) | 106 | -0.92c | 44% |
| p_24h (alerted only) | 81 | -0.11c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

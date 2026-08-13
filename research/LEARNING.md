# What the scanner has learned about itself

_Auto-generated 2026-08-13T14:25:19Z. 10000 candidates logged, 5768 with a filled 24h forward price._

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
| filtered out | 5451 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 81 | -0.11c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 236 | -0.82c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 163 | +1.49c | +0.00c | 54% | FOLLOW |
| thin_market | 69 | +1.29c | +0.45c | 66% | FOLLOW |
| repeat_actor | 1398 | +0.66c | +0.10c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 25 | +0.53c | -0.05c | 41% | INSUFFICIENT DATA |
| large_trade | 1977 | +0.49c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 837 | +0.46c | +0.10c | 58% | NOISE (no measurable edge) |
| volume_spike | 4970 | +0.19c | -0.00c | 50% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| price_jump | 907 | -0.02c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 516 | -0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 260 | -0.43c | -0.50c | 47% | NOISE (no measurable edge) |
| coordination | 5 | -1.15c | -0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2626 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2407 | +0.16c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 558 | -0.04c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 151 | -1.03c | +0.00c | 44% | FADE (signal points the wrong way) |
| sports | 26 | -4.88c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 864 | +0.47c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 818 | +0.35c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 607 | +0.29c | +0.00c | 57% | NOISE (no measurable edge) |
| under 40 | 3479 | -0.10c | -0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5252 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 516 | -0.23c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 392 | +1.39c | +0.37c | 57% | FOLLOW |
| 1 to 4 weeks | 1360 | +0.42c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3491 | -0.07c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 355 | -0.31c | +0.10c | 53% | NOISE (no measurable edge) |
| under 1 day | 67 | -1.19c | +0.95c | 55% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 111 | +0.33c | 48% |
| p_6h (alerted only) | 105 | -0.93c | 44% |
| p_24h (alerted only) | 81 | -0.11c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

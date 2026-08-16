# What the scanner has learned about itself

_Auto-generated 2026-08-16T01:53:17Z. 10000 candidates logged, 5691 with a filled 24h forward price._

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
| alerted (passed gate and score) | 65 | +0.78c | +0.45c | 52% | NOISE (no measurable edge) |
| filtered out | 5417 | +0.14c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 209 | -0.88c | -0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 68 | +1.55c | +0.37c | 69% | FOLLOW |
| cross_platform | 150 | +1.13c | +0.00c | 52% | FOLLOW |
| within_trader | 761 | +1.04c | +0.10c | 59% | FOLLOW |
| repeat_actor | 1272 | +0.87c | +0.10c | 59% | NOISE (no measurable edge) |
| large_trade | 1820 | +0.76c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4920 | +0.23c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 499 | +0.11c | -0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 881 | -0.44c | -0.00c | 49% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 257 | -0.64c | -0.50c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 26 | -0.95c | -0.08c | 42% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 608 | +0.34c | -0.00c | 54% | NOISE (no measurable edge) |
| entertainment | 129 | +0.21c | -0.50c | 42% | NOISE (no measurable edge) |
| other | 2364 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2572 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| sports | 18 | -4.58c | -1.50c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 805 | +0.83c | +0.05c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 797 | +0.31c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 559 | +0.27c | -0.00c | 55% | NOISE (no measurable edge) |
| under 40 | 3530 | -0.13c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 499 | +0.11c | -0.00c | 53% | NOISE (no measurable edge) |
| normal | 5192 | +0.11c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 63 | +1.60c | +0.40c | 54% | FOLLOW |
| 3 to 7 days | 419 | +1.28c | +0.25c | 55% | FOLLOW |
| 1 to 3 days | 334 | +0.69c | +0.28c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1274 | +0.46c | +0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3493 | -0.18c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 92 | +0.01c | 49% |
| p_6h (alerted only) | 87 | +0.13c | 44% |
| p_24h (alerted only) | 65 | +0.78c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

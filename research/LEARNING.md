# What the scanner has learned about itself

_Auto-generated 2026-08-14T11:53:01Z. 10000 candidates logged, 5561 with a filled 24h forward price._

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
| alerted (passed gate and score) | 75 | +0.44c | +1.00c | 52% | NOISE (no measurable edge) |
| filtered out | 5265 | +0.16c | -0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 221 | -0.81c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 68 | +1.68c | +0.47c | 68% | FOLLOW |
| cross_platform | 160 | +1.53c | +0.00c | 54% | FOLLOW |
| fresh_wallet | 23 | +1.05c | +0.00c | 48% | INSUFFICIENT DATA |
| within_trader | 777 | +0.79c | +0.10c | 59% | NOISE (no measurable edge) |
| repeat_actor | 1315 | +0.74c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1864 | +0.68c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4799 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 478 | +0.16c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 858 | -0.16c | -0.00c | 51% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 261 | -0.53c | -0.55c | 45% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 129 | +0.27c | +0.00c | 44% | NOISE (no measurable edge) |
| crypto | 549 | +0.21c | +0.00c | 52% | NOISE (no measurable edge) |
| politics | 2389 | +0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2472 | +0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| sports | 22 | -4.43c | -3.00c | 29% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 834 | +0.62c | +0.05c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 777 | +0.44c | +0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 566 | +0.31c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3384 | -0.10c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 478 | +0.16c | +0.00c | 53% | NOISE (no measurable edge) |
| normal | 5083 | +0.12c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 392 | +1.58c | +0.33c | 58% | FOLLOW |
| under 1 day | 65 | +1.31c | +0.95c | 57% | FOLLOW |
| 1 to 4 weeks | 1313 | +0.38c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3373 | -0.08c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 321 | -0.10c | +0.10c | 54% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 107 | +0.15c | 44% |
| p_6h (alerted only) | 103 | -0.25c | 45% |
| p_24h (alerted only) | 75 | +0.44c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

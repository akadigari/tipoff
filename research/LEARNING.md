# What the scanner has learned about itself

_Auto-generated 2026-08-15T08:40:10Z. 10000 candidates logged, 5585 with a filled 24h forward price._

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
| alerted (passed gate and score) | 71 | +0.64c | +1.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5306 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 208 | -1.06c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 67 | +1.69c | +0.50c | 68% | FOLLOW |
| cross_platform | 156 | +1.07c | +0.00c | 50% | FOLLOW |
| within_trader | 746 | +0.94c | +0.10c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1269 | +0.90c | +0.15c | 60% | NOISE (no measurable edge) |
| large_trade | 1820 | +0.80c | +0.10c | 58% | NOISE (no measurable edge) |
| volume_spike | 4808 | +0.24c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 480 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 24 | -0.01c | -0.03c | 45% | INSUFFICIENT DATA |
| price_jump | 889 | -0.24c | -0.00c | 50% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 257 | -0.75c | -0.50c | 45% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 564 | +0.30c | +0.00c | 53% | NOISE (no measurable edge) |
| other | 2415 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2460 | +0.12c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 127 | -0.24c | -0.00c | 43% | NOISE (no measurable edge) |
| sports | 19 | -4.58c | -2.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 809 | +0.88c | +0.10c | 58% | NOISE (no measurable edge) |
| 40 to 54 | 796 | +0.36c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 554 | +0.14c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3426 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5105 | +0.15c | +0.00c | 51% | NOISE (no measurable edge) |
| high | 480 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 61 | +1.85c | +0.40c | 54% | FOLLOW |
| 3 to 7 days | 418 | +1.40c | +0.27c | 56% | FOLLOW |
| 1 to 4 weeks | 1263 | +0.58c | +0.05c | 54% | NOISE (no measurable edge) |
| 1 to 3 days | 329 | +0.01c | +0.25c | 54% | NOISE (no measurable edge) |
| over a month | 3414 | -0.12c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 98 | -0.18c | 46% |
| p_6h (alerted only) | 94 | -0.25c | 44% |
| p_24h (alerted only) | 71 | +0.64c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

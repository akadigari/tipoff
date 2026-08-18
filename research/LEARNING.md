# What the scanner has learned about itself

_Auto-generated 2026-08-18T19:35:11Z. 10000 candidates logged, 5538 with a filled 24h forward price._

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
| filtered out | 5310 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 41 | -0.65c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 187 | -0.77c | +0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 66 | +0.76c | +0.10c | 67% | NOISE (no measurable edge) |
| within_trader | 759 | +0.64c | +0.05c | 59% | NOISE (no measurable edge) |
| large_trade | 1776 | +0.22c | +0.00c | 56% | NOISE (no measurable edge) |
| repeat_actor | 1250 | +0.19c | +0.05c | 57% | NOISE (no measurable edge) |
| coordination | 9 | +0.13c | +0.50c | 75% | INSUFFICIENT DATA |
| volume_spike | 4877 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 216 | +0.05c | -0.48c | 47% | NOISE (no measurable edge) |
| cross_platform | 130 | +0.03c | +0.00c | 46% | NOISE (no measurable edge) |
| insiderable | 502 | -0.19c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 32 | -0.22c | -0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 769 | -1.21c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 676 | +0.40c | +0.00c | 55% | NOISE (no measurable edge) |
| politics | 2507 | -0.03c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2236 | -0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 106 | -1.41c | +0.00c | 48% | FADE (signal points the wrong way) |
| sports | 13 | -3.77c | -1.00c | 38% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 811 | +0.18c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 549 | +0.10c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3426 | -0.10c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 752 | -0.33c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5036 | -0.06c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 502 | -0.19c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 74 | +2.03c | +0.00c | 51% | FOLLOW |
| 3 to 7 days | 352 | +0.87c | +0.30c | 56% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1243 | +0.13c | -0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3427 | -0.14c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 301 | -1.18c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 71 | -0.24c | 45% |
| p_6h (alerted only) | 59 | -0.61c | 44% |
| p_24h (alerted only) | 41 | -0.65c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

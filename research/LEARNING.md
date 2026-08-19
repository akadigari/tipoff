# What the scanner has learned about itself

_Auto-generated 2026-08-19T06:59:48Z. 10000 candidates logged, 5438 with a filled 24h forward price._

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
| alerted (passed gate and score) | 40 | -0.08c | +0.22c | 53% | NOISE (no measurable edge) |
| filtered out | 5216 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 182 | -0.90c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 57 | +0.52c | +0.05c | 63% | NOISE (no measurable edge) |
| within_trader | 739 | +0.34c | -0.00c | 57% | NOISE (no measurable edge) |
| cross_platform | 133 | +0.05c | -0.00c | 47% | NOISE (no measurable edge) |
| coordination | 8 | +0.02c | +0.40c | 71% | INSUFFICIENT DATA |
| repeat_actor | 1202 | +0.00c | +0.02c | 56% | NOISE (no measurable edge) |
| large_trade | 1698 | +0.00c | +0.00c | 55% | NOISE (no measurable edge) |
| price_impact | 211 | -0.01c | -0.55c | 45% | NOISE (no measurable edge) |
| volume_spike | 4793 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 30 | -0.11c | +0.02c | 54% | NOISE (no measurable edge) |
| insiderable | 497 | -0.34c | -0.00c | 51% | NOISE (no measurable edge) |
| price_jump | 747 | -1.05c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 675 | +0.41c | +0.00c | 55% | NOISE (no measurable edge) |
| politics | 2498 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2148 | -0.20c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 107 | -1.90c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 10 | -4.70c | -3.50c | 30% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 782 | +0.04c | +0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 523 | -0.06c | -0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3378 | -0.12c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 755 | -0.44c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4941 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 497 | -0.34c | -0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 75 | +1.29c | -0.00c | 48% | FOLLOW |
| 3 to 7 days | 317 | +0.32c | +0.10c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1213 | -0.00c | -0.00c | 50% | NOISE (no measurable edge) |
| over a month | 3422 | -0.13c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 276 | -1.20c | +0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 66 | -0.07c | 48% |
| p_6h (alerted only) | 59 | -0.17c | 46% |
| p_24h (alerted only) | 40 | -0.08c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

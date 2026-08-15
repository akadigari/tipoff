# What the scanner has learned about itself

_Auto-generated 2026-08-15T15:30:56Z. 10000 candidates logged, 5585 with a filled 24h forward price._

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
| alerted (passed gate and score) | 69 | +1.11c | +1.00c | 53% | FOLLOW |
| filtered out | 5307 | +0.22c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 209 | -1.07c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 65 | +1.70c | +0.50c | 69% | FOLLOW |
| within_trader | 738 | +1.10c | +0.15c | 61% | FOLLOW |
| cross_platform | 155 | +1.09c | +0.00c | 50% | FOLLOW |
| repeat_actor | 1265 | +0.99c | +0.15c | 60% | NOISE (no measurable edge) |
| large_trade | 1814 | +0.87c | +0.10c | 59% | NOISE (no measurable edge) |
| volume_spike | 4805 | +0.27c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 483 | +0.21c | +0.00c | 55% | NOISE (no measurable edge) |
| fresh_wallet | 25 | -0.02c | -0.05c | 43% | INSUFFICIENT DATA |
| price_jump | 901 | -0.04c | -0.00c | 50% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 251 | -0.67c | -0.50c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 580 | +0.33c | +0.00c | 53% | NOISE (no measurable edge) |
| other | 2383 | +0.25c | -0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 126 | +0.20c | -0.25c | 43% | NOISE (no measurable edge) |
| politics | 2478 | +0.11c | +0.00c | 51% | NOISE (no measurable edge) |
| sports | 18 | -4.58c | -1.50c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 807 | +0.98c | +0.10c | 58% | NOISE (no measurable edge) |
| 40 to 54 | 793 | +0.39c | +0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 553 | +0.32c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3432 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 483 | +0.21c | +0.00c | 55% | NOISE (no measurable edge) |
| normal | 5102 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 61 | +1.85c | +0.40c | 54% | FOLLOW |
| 3 to 7 days | 418 | +1.48c | +0.30c | 56% | FOLLOW |
| 1 to 3 days | 331 | +0.67c | +0.30c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1269 | +0.59c | +0.05c | 54% | NOISE (no measurable edge) |
| over a month | 3406 | -0.14c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 96 | -0.08c | 46% |
| p_6h (alerted only) | 92 | -0.02c | 45% |
| p_24h (alerted only) | 69 | +1.11c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

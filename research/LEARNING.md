# What the scanner has learned about itself

_Auto-generated 2026-08-22T14:31:11Z. 10000 candidates logged, 5526 with a filled 24h forward price._

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
| alerted (passed gate and score) | 48 | +2.04c | +0.22c | 51% | FOLLOW |
| filtered out | 5296 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 182 | -1.00c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 232 | +2.12c | +0.75c | 53% | FOLLOW |
| cross_platform | 96 | +0.95c | +0.00c | 49% | NOISE (no measurable edge) |
| volume_spike | 4892 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 755 | -0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 758 | -0.22c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 468 | -0.30c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1677 | -0.65c | -0.00c | 52% | NOISE (no measurable edge) |
| thin_market | 42 | -0.75c | +0.08c | 58% | NOISE (no measurable edge) |
| repeat_actor | 1229 | -0.79c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 18 | -1.01c | +0.00c | 47% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1069 | +0.78c | +0.20c | 56% | NOISE (no measurable edge) |
| politics | 2203 | +0.04c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2172 | -0.42c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 82 | -2.02c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3482 | +0.15c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 699 | +0.11c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 543 | -0.34c | +0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 802 | -0.71c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5058 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 468 | -0.30c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 43 | +4.79c | -0.00c | 46% | FOLLOW |
| 3 to 7 days | 232 | +0.87c | +0.17c | 52% | NOISE (no measurable edge) |
| 1 to 3 days | 293 | +0.41c | +0.35c | 56% | NOISE (no measurable edge) |
| over a month | 3491 | -0.03c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1314 | -0.57c | +0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 88 | +1.68c | 56% |
| p_6h (alerted only) | 75 | +3.11c | 55% |
| p_24h (alerted only) | 48 | +2.04c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

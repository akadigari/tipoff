# What the scanner has learned about itself

_Auto-generated 2026-08-11T16:07:26Z. 10000 candidates logged, 5679 with a filled 24h forward price._

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
| alerted (passed gate and score) | 83 | +1.13c | +1.00c | 53% | FOLLOW |
| filtered out | 5350 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 246 | -0.44c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 166 | +1.06c | +0.00c | 51% | FOLLOW |
| thin_market | 69 | +0.83c | +0.30c | 62% | NOISE (no measurable edge) |
| fresh_wallet | 21 | +0.82c | -0.10c | 45% | INSUFFICIENT DATA |
| repeat_actor | 1378 | +0.34c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1976 | +0.32c | +0.05c | 57% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4848 | -0.00c | +0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 943 | -0.05c | -0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 837 | -0.10c | +0.05c | 58% | NOISE (no measurable edge) |
| insiderable | 496 | -0.41c | +0.00c | 46% | NOISE (no measurable edge) |
| price_impact | 262 | -1.15c | -0.50c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2315 | +0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 492 | +0.02c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2649 | -0.17c | -0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 197 | -0.39c | -0.05c | 43% | NOISE (no measurable edge) |
| sports | 26 | -4.67c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 831 | +0.37c | +0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 802 | +0.26c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3422 | -0.23c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 624 | -0.32c | -0.00c | 58% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5183 | -0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 496 | -0.41c | +0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 371 | +1.61c | +0.40c | 57% | FOLLOW |
| 1 to 4 weeks | 1165 | +0.54c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3578 | -0.30c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 421 | -1.08c | +0.05c | 51% | FADE (signal points the wrong way) |
| under 1 day | 63 | -4.40c | +0.00c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 113 | +0.53c | 47% |
| p_6h (alerted only) | 110 | -0.77c | 43% |
| p_24h (alerted only) | 83 | +1.13c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

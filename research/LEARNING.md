# What the scanner has learned about itself

_Auto-generated 2026-08-09T02:23:01Z. 10000 candidates logged, 5811 with a filled 24h forward price._

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
| alerted (passed gate and score) | 80 | +1.31c | +1.00c | 55% | FOLLOW |
| filtered out | 5494 | -0.31c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 237 | -0.89c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 149 | +0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| fresh_wallet | 19 | +0.02c | +0.15c | 56% | INSUFFICIENT DATA |
| large_trade | 1989 | -0.16c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4862 | -0.20c | +0.00c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1372 | -0.21c | +0.05c | 55% | NOISE (no measurable edge) |
| insiderable | 538 | -0.24c | +0.00c | 47% | NOISE (no measurable edge) |
| coordination | 2 | -0.37c | -0.37c | 50% | INSUFFICIENT DATA |
| thin_market | 41 | -0.55c | +0.00c | 51% | NOISE (no measurable edge) |
| price_jump | 1085 | -0.59c | -0.50c | 48% | NOISE (no measurable edge) |
| within_trader | 859 | -0.67c | +0.00c | 55% | NOISE (no measurable edge) |
| price_impact | 281 | -1.07c | -1.00c | 44% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 513 | -0.04c | +0.00c | 47% | NOISE (no measurable edge) |
| politics | 2363 | -0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2607 | -0.51c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 311 | -0.64c | -0.25c | 44% | NOISE (no measurable edge) |
| sports | 17 | -5.97c | -5.50c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 869 | -0.01c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 803 | -0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3518 | -0.34c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 621 | -0.90c | +0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 538 | -0.24c | +0.00c | 47% | NOISE (no measurable edge) |
| normal | 5273 | -0.32c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 535 | +0.10c | +0.05c | 51% | NOISE (no measurable edge) |
| 1 to 4 weeks | 925 | -0.18c | -0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3827 | -0.22c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 401 | -2.06c | -0.15c | 49% | FADE (signal points the wrong way) |
| under 1 day | 35 | -4.53c | +0.30c | 58% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.53c | 46% |
| p_6h (alerted only) | 108 | -0.76c | 46% |
| p_24h (alerted only) | 80 | +1.31c | 55% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

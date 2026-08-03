# What the scanner has learned about itself

_Auto-generated 2026-08-03T11:38:58Z. 10000 candidates logged, 5864 with a filled 24h forward price._

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
| alerted (passed gate and score) | 65 | +0.11c | -1.00c | 48% | NOISE (no measurable edge) |
| filtered out | 5568 | -0.40c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 231 | -0.61c | +0.00c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 15 | +2.37c | +0.65c | 60% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 12 | +0.72c | +1.50c | 73% | INSUFFICIENT DATA |
| large_trade | 2073 | -0.27c | +0.00c | 54% | NOISE (no measurable edge) |
| volume_spike | 4846 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1433 | -0.31c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 640 | -0.44c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 854 | -0.72c | +0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 112 | -0.73c | +0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 1205 | -0.95c | -0.75c | 47% | NOISE (no measurable edge) |
| price_impact | 283 | -1.24c | -1.00c | 45% | FADE (signal points the wrong way) |
| thin_market | 46 | -1.90c | -0.30c | 38% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 374 | +0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 554 | -0.15c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2292 | -0.25c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2623 | -0.66c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 21 | -1.02c | -0.50c | 39% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 883 | -0.18c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3479 | -0.30c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 837 | -0.58c | +0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 665 | -1.02c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5224 | -0.40c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 640 | -0.44c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 26 | +3.00c | +0.97c | 54% | INSUFFICIENT DATA |
| 3 to 7 days | 558 | +0.47c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3802 | -0.34c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 997 | -0.78c | +0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 381 | -1.48c | -0.10c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 88 | +0.71c | 44% |
| p_6h (alerted only) | 82 | -0.56c | 45% |
| p_24h (alerted only) | 65 | +0.11c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-04T15:32:20Z. 10000 candidates logged, 5818 with a filled 24h forward price._

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
| alerted (passed gate and score) | 71 | -0.21c | -0.20c | 46% | NOISE (no measurable edge) |
| filtered out | 5511 | -0.39c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 236 | -0.56c | +0.00c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 17 | +2.48c | +0.15c | 56% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4789 | -0.28c | -0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2058 | -0.35c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1427 | -0.35c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 617 | -0.61c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 283 | -0.67c | -0.50c | 47% | NOISE (no measurable edge) |
| cross_platform | 109 | -0.72c | -0.00c | 45% | NOISE (no measurable edge) |
| within_trader | 864 | -0.72c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 1206 | -1.02c | -1.00c | 47% | FADE (signal points the wrong way) |
| thin_market | 46 | -1.60c | -0.15c | 41% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 534 | +0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2279 | -0.23c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 371 | -0.26c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2611 | -0.67c | -0.00c | 47% | NOISE (no measurable edge) |
| sports | 23 | -1.57c | -1.00c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 880 | -0.28c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3465 | -0.29c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 817 | -0.54c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 656 | -0.92c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5201 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 617 | -0.61c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 552 | +0.38c | +0.30c | 52% | NOISE (no measurable edge) |
| over a month | 3774 | -0.31c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 965 | -0.51c | -0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 396 | -1.91c | -0.30c | 48% | FADE (signal points the wrong way) |
| under 1 day | 32 | -3.26c | +0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 98 | +0.45c | 42% |
| p_6h (alerted only) | 90 | -0.87c | 44% |
| p_24h (alerted only) | 71 | -0.21c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

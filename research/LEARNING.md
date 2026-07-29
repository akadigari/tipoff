# What the scanner has learned about itself

_Auto-generated 2026-07-29T10:47:35Z. 10000 candidates logged, 5794 with a filled 24h forward price._

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
| filtered out | 5488 | -0.38c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 78 | -1.02c | -0.83c | 43% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 228 | -1.50c | +0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 17 | +1.32c | -0.10c | 44% | INSUFFICIENT DATA |
| chatter | 4 | +1.19c | +0.58c | 75% | INSUFFICIENT DATA |
| repeat_actor | 1245 | -0.01c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1904 | -0.11c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 832 | -0.14c | +0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4649 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 350 | -0.34c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 671 | -0.85c | -0.00c | 46% | NOISE (no measurable edge) |
| thin_market | 36 | -1.42c | -0.37c | 41% | FADE (signal points the wrong way) |
| price_jump | 1303 | -1.62c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 90 | -2.85c | -0.03c | 42% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 32 | +0.31c | +0.00c | 58% | NOISE (no measurable edge) |
| crypto | 573 | -0.08c | +0.00c | 52% | NOISE (no measurable edge) |
| other | 2649 | -0.40c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2140 | -0.47c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 400 | -1.01c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 861 | -0.18c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3495 | -0.29c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 583 | -0.92c | -0.00c | 49% | NOISE (no measurable edge) |
| 40 to 54 | 855 | -0.93c | -0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5123 | -0.38c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 671 | -0.85c | -0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 20 | +9.76c | +5.52c | 60% | INSUFFICIENT DATA |
| 1 to 3 days | 250 | +0.14c | +0.40c | 52% | NOISE (no measurable edge) |
| 3 to 7 days | 453 | +0.05c | +0.15c | 52% | NOISE (no measurable edge) |
| over a month | 3483 | -0.32c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1491 | -1.05c | -0.05c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | -0.04c | 46% |
| p_6h (alerted only) | 104 | -0.61c | 48% |
| p_24h (alerted only) | 78 | -1.02c | 43% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

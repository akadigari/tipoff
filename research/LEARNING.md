# What the scanner has learned about itself

_Auto-generated 2026-07-24T18:39:41Z. 10000 candidates logged, 5889 with a filled 24h forward price._

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
| alerted (passed gate and score) | 105 | -0.38c | -0.50c | 41% | NOISE (no measurable edge) |
| filtered out | 5551 | -0.42c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 233 | -1.89c | +0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1070 | +0.06c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 780 | -0.05c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1801 | -0.13c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4786 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 345 | -0.46c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 595 | -0.74c | -0.00c | 45% | NOISE (no measurable edge) |
| price_jump | 1303 | -1.91c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 88 | -2.07c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 30 | -3.47c | -0.50c | 32% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 62 | +0.56c | +0.28c | 57% | NOISE (no measurable edge) |
| crypto | 670 | -0.28c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2783 | -0.46c | -0.00c | 48% | NOISE (no measurable edge) |
| politics | 2052 | -0.52c | +0.00c | 43% | NOISE (no measurable edge) |
| entertainment | 322 | -1.06c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3651 | -0.40c | -0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 871 | -0.43c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 795 | -0.57c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 572 | -0.99c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5294 | -0.45c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 595 | -0.74c | -0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 19 | +3.64c | +1.95c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 233 | +0.64c | +0.50c | 55% | NOISE (no measurable edge) |
| over a month | 3463 | -0.48c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 3 days | 209 | -0.52c | -0.30c | 49% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1877 | -0.71c | -0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 150 | -0.82c | 42% |
| p_6h (alerted only) | 139 | -1.40c | 44% |
| p_24h (alerted only) | 105 | -0.38c | 41% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

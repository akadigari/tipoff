# What the scanner has learned about itself

_Auto-generated 2026-08-24T14:53:26Z. 10000 candidates logged, 5738 with a filled 24h forward price._

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
| filtered out | 5474 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 57 | -0.27c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 207 | -1.10c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 281 | +1.29c | -0.00c | 50% | FOLLOW |
| cross_platform | 91 | +1.01c | +0.00c | 49% | FOLLOW |
| volume_spike | 5074 | -0.05c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 851 | -0.09c | -0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 529 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.30c | -0.00c | 43% | INSUFFICIENT DATA |
| price_jump | 771 | -0.34c | -0.10c | 49% | NOISE (no measurable edge) |
| large_trade | 1878 | -0.58c | +0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1377 | -0.67c | -0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 39 | -2.07c | +0.05c | 56% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1303 | +0.35c | +0.05c | 53% | NOISE (no measurable edge) |
| politics | 2119 | +0.15c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2220 | -0.46c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 96 | -0.94c | +0.00c | 44% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 747 | +0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3472 | +0.10c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 627 | -0.31c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 892 | -0.83c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5209 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 529 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 41 | +4.36c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 228 | +0.99c | +0.30c | 53% | NOISE (no measurable edge) |
| over a month | 3582 | +0.01c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 284 | -0.15c | +0.50c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1473 | -0.60c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | +1.31c | 58% |
| p_6h (alerted only) | 83 | +1.89c | 51% |
| p_24h (alerted only) | 57 | -0.27c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

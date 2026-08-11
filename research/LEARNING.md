# What the scanner has learned about itself

_Auto-generated 2026-08-11T09:11:03Z. 10000 candidates logged, 5663 with a filled 24h forward price._

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
| alerted (passed gate and score) | 88 | +1.62c | +1.00c | 53% | FOLLOW |
| filtered out | 5332 | -0.18c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 243 | -0.49c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 163 | +1.39c | +0.00c | 52% | FOLLOW |
| fresh_wallet | 20 | +0.87c | -0.05c | 47% | INSUFFICIENT DATA |
| thin_market | 69 | +0.77c | +0.30c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1373 | +0.30c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1961 | +0.28c | +0.05c | 57% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4820 | -0.04c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 837 | -0.12c | +0.05c | 58% | NOISE (no measurable edge) |
| insiderable | 500 | -0.28c | +0.00c | 46% | NOISE (no measurable edge) |
| price_jump | 952 | -0.35c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 268 | -1.32c | -0.63c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 207 | +0.33c | +0.00c | 46% | NOISE (no measurable edge) |
| politics | 2324 | +0.12c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 479 | -0.36c | -0.00c | 44% | NOISE (no measurable edge) |
| other | 2630 | -0.38c | +0.00c | 49% | NOISE (no measurable edge) |
| sports | 23 | -5.52c | -5.50c | 23% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 779 | +0.41c | +0.00c | 52% | NOISE (no measurable edge) |
| 55 to 69 | 829 | +0.29c | -0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3429 | -0.37c | -0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 626 | -0.38c | +0.00c | 58% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5163 | -0.16c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 500 | -0.28c | +0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 380 | +1.33c | +0.42c | 57% | FOLLOW |
| 1 to 4 weeks | 1112 | +0.40c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3600 | -0.31c | -0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 431 | -1.52c | +0.00c | 50% | FADE (signal points the wrong way) |
| under 1 day | 56 | -4.01c | +0.13c | 54% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 115 | +0.54c | 47% |
| p_6h (alerted only) | 112 | -0.50c | 45% |
| p_24h (alerted only) | 88 | +1.62c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

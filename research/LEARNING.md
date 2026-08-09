# What the scanner has learned about itself

_Auto-generated 2026-08-09T15:40:39Z. 10000 candidates logged, 5790 with a filled 24h forward price._

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
| alerted (passed gate and score) | 84 | +1.50c | +1.00c | 55% | FOLLOW |
| filtered out | 5470 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 236 | -0.91c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 159 | +0.56c | +0.00c | 51% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| thin_market | 50 | +0.09c | -0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1962 | -0.12c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1354 | -0.12c | +0.05c | 55% | NOISE (no measurable edge) |
| volume_spike | 4850 | -0.20c | +0.00c | 49% | NOISE (no measurable edge) |
| coordination | 2 | -0.37c | -0.37c | 50% | INSUFFICIENT DATA |
| insiderable | 520 | -0.47c | +0.00c | 44% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.56c | +0.00c | 50% | INSUFFICIENT DATA |
| price_jump | 1062 | -0.59c | -0.50c | 48% | NOISE (no measurable edge) |
| within_trader | 852 | -0.67c | +0.00c | 55% | NOISE (no measurable edge) |
| price_impact | 286 | -1.11c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2351 | +0.02c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 523 | -0.18c | -0.00c | 46% | NOISE (no measurable edge) |
| other | 2609 | -0.55c | -0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 290 | -0.84c | -0.32c | 44% | NOISE (no measurable edge) |
| sports | 17 | -5.97c | -5.50c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 808 | +0.16c | +0.00c | 52% | NOISE (no measurable edge) |
| 55 to 69 | 852 | -0.18c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3524 | -0.37c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 606 | -0.86c | +0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5270 | -0.30c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 520 | -0.47c | +0.00c | 44% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 504 | +0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| 1 to 4 weeks | 964 | -0.14c | +0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3782 | -0.22c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 415 | -1.95c | -0.20c | 49% | FADE (signal points the wrong way) |
| under 1 day | 45 | -4.38c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 110 | +0.65c | 47% |
| p_6h (alerted only) | 108 | -0.50c | 46% |
| p_24h (alerted only) | 84 | +1.50c | 55% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-09-01T13:27:27Z. 10000 candidates logged, 6584 with a filled 24h forward price._

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
| alerted (passed gate and score) | 70 | +1.87c | +0.00c | 51% | FOLLOW |
| filtered out | 6262 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 252 | -1.34c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 24 | +0.39c | +0.00c | 45% | INSUFFICIENT DATA |
| price_impact | 347 | +0.17c | -1.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 74 | +0.10c | +0.00c | 41% | NOISE (no measurable edge) |
| insiderable | 592 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 5793 | -0.10c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 971 | -0.33c | +0.00c | 54% | NOISE (no measurable edge) |
| large_trade | 2263 | -0.40c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1645 | -0.51c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 929 | -0.76c | -0.65c | 48% | NOISE (no measurable edge) |
| coordination | 9 | -1.01c | -0.00c | 50% | INSUFFICIENT DATA |
| thin_market | 42 | -2.34c | +0.08c | 58% | FADE (signal points the wrong way) |
| chatter | 6 | -3.58c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2329 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2585 | -0.11c | -0.00c | 48% | NOISE (no measurable edge) |
| crypto | 1556 | -0.18c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 114 | -1.50c | -0.50c | 39% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3900 | +0.11c | +0.00c | 48% | NOISE (no measurable edge) |
| 40 to 54 | 866 | -0.08c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 1046 | -0.53c | -0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 772 | -0.73c | -0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 592 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| normal | 5992 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 563 | +0.66c | +0.30c | 55% | NOISE (no measurable edge) |
| over a month | 4131 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1468 | -0.62c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 314 | -0.63c | +0.18c | 51% | NOISE (no measurable edge) |
| under 1 day | 15 | -4.04c | -7.50c | 47% | INSUFFICIENT DATA |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 102 | +1.18c | 55% |
| p_6h (alerted only) | 94 | +2.91c | 55% |
| p_24h (alerted only) | 70 | +1.87c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

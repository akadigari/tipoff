# What the scanner has learned about itself

_Auto-generated 2026-08-24T21:38:17Z. 10000 candidates logged, 5693 with a filled 24h forward price._

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
| filtered out | 5429 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 56 | -0.62c | -0.25c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 208 | -1.02c | +0.00c | 52% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 89 | +0.91c | -0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 285 | +0.89c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 850 | -0.03c | -0.00c | 54% | NOISE (no measurable edge) |
| volume_spike | 5038 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 522 | -0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 761 | -0.36c | -0.10c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 15 | -0.36c | -0.00c | 42% | INSUFFICIENT DATA |
| coordination | 8 | -0.49c | +0.55c | 86% | INSUFFICIENT DATA |
| large_trade | 1879 | -0.56c | +0.00c | 51% | NOISE (no measurable edge) |
| repeat_actor | 1385 | -0.66c | -0.00c | 53% | NOISE (no measurable edge) |
| thin_market | 31 | -3.16c | -0.15c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1321 | +0.35c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2093 | +0.08c | -0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 92 | -0.31c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2187 | -0.38c | -0.00c | 45% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 738 | +0.24c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3433 | +0.15c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 633 | -0.40c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 889 | -0.75c | +0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5171 | -0.03c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 522 | -0.09c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 38 | +5.18c | +0.00c | 48% | FOLLOW |
| 3 to 7 days | 227 | +1.34c | +0.25c | 52% | FOLLOW |
| 1 to 3 days | 264 | +0.37c | +0.53c | 56% | NOISE (no measurable edge) |
| over a month | 3555 | +0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1489 | -0.63c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | +1.29c | 57% |
| p_6h (alerted only) | 82 | +1.97c | 52% |
| p_24h (alerted only) | 56 | -0.62c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

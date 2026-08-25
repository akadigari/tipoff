# What the scanner has learned about itself

_Auto-generated 2026-08-25T07:02:35Z. 10000 candidates logged, 5629 with a filled 24h forward price._

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
| filtered out | 5364 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 209 | -0.81c | +0.00c | 52% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 56 | -0.90c | -0.50c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 83 | +1.01c | +0.00c | 47% | FOLLOW |
| price_impact | 291 | +0.68c | -0.50c | 48% | NOISE (no measurable edge) |
| within_trader | 836 | +0.05c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4965 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 525 | -0.07c | -0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 15 | -0.27c | -0.05c | 38% | INSUFFICIENT DATA |
| price_jump | 770 | -0.34c | -0.00c | 50% | NOISE (no measurable edge) |
| large_trade | 1838 | -0.51c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1363 | -0.61c | +0.00c | 54% | NOISE (no measurable edge) |
| coordination | 7 | -0.63c | +0.60c | 83% | INSUFFICIENT DATA |
| thin_market | 35 | -2.72c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1320 | +0.29c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2039 | +0.06c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2178 | -0.36c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 92 | -0.80c | +0.00c | 42% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 728 | +0.14c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3402 | +0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 640 | -0.38c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 859 | -0.61c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5104 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 525 | -0.07c | -0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 37 | +4.93c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 221 | +1.53c | +0.40c | 54% | FOLLOW |
| 1 to 3 days | 253 | +0.04c | +0.50c | 55% | NOISE (no measurable edge) |
| over a month | 3497 | +0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1505 | -0.69c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 98 | +1.11c | 55% |
| p_6h (alerted only) | 82 | +2.52c | 52% |
| p_24h (alerted only) | 56 | -0.90c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-22T01:45:11Z. 10000 candidates logged, 5410 with a filled 24h forward price._

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
| alerted (passed gate and score) | 43 | +3.34c | +0.45c | 52% | FOLLOW |
| filtered out | 5194 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 173 | -0.56c | -0.00c | 54% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 226 | +1.64c | +0.50c | 53% | FOLLOW |
| cross_platform | 108 | +0.86c | +0.00c | 48% | NOISE (no measurable edge) |
| volume_spike | 4787 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 719 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 737 | -0.07c | +0.00c | 56% | NOISE (no measurable edge) |
| insiderable | 463 | -0.35c | -0.00c | 46% | NOISE (no measurable edge) |
| large_trade | 1616 | -0.59c | +0.00c | 53% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1171 | -0.69c | +0.00c | 55% | NOISE (no measurable edge) |
| fresh_wallet | 21 | -0.80c | +0.05c | 56% | INSUFFICIENT DATA |
| thin_market | 40 | -0.89c | +0.08c | 58% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 949 | +0.79c | +0.20c | 56% | NOISE (no measurable edge) |
| politics | 2251 | +0.05c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2122 | -0.38c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 88 | -1.68c | +0.00c | 45% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3433 | +0.14c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 688 | +0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 518 | -0.07c | +0.00c | 56% | NOISE (no measurable edge) |
| 55 to 69 | 771 | -0.69c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4947 | +0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 463 | -0.35c | -0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 49 | +4.69c | +0.00c | 49% | FOLLOW |
| 1 to 3 days | 283 | +0.75c | +0.30c | 55% | NOISE (no measurable edge) |
| 3 to 7 days | 241 | +0.64c | +0.10c | 51% | NOISE (no measurable edge) |
| over a month | 3415 | -0.03c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1273 | -0.61c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 83 | +1.77c | 57% |
| p_6h (alerted only) | 71 | +3.11c | 54% |
| p_24h (alerted only) | 43 | +3.34c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

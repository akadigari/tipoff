# What the scanner has learned about itself

_Auto-generated 2026-08-21T15:42:37Z. 10000 candidates logged, 5381 with a filled 24h forward price._

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
| alerted (passed gate and score) | 44 | +3.41c | +0.47c | 53% | FOLLOW |
| filtered out | 5167 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 170 | -0.86c | +0.00c | 53% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 113 | +0.89c | -0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 727 | +0.11c | -0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4746 | +0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 219 | +0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| coordination | 9 | -0.24c | +0.60c | 88% | INSUFFICIENT DATA |
| thin_market | 42 | -0.29c | +0.10c | 65% | NOISE (no measurable edge) |
| insiderable | 448 | -0.30c | +0.00c | 46% | NOISE (no measurable edge) |
| large_trade | 1604 | -0.38c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 22 | -0.47c | +0.05c | 58% | INSUFFICIENT DATA |
| repeat_actor | 1151 | -0.47c | +0.05c | 56% | NOISE (no measurable edge) |
| price_jump | 730 | -0.63c | -0.50c | 48% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 906 | +0.66c | +0.17c | 57% | NOISE (no measurable edge) |
| politics | 2302 | -0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2076 | -0.30c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 97 | -2.13c | -1.00c | 41% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 504 | +0.26c | +0.00c | 57% | NOISE (no measurable edge) |
| under 40 | 3434 | +0.06c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 679 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 764 | -0.76c | +0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4933 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 448 | -0.30c | +0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 50 | +4.54c | +0.00c | 48% | FOLLOW |
| 3 to 7 days | 243 | +0.62c | +0.35c | 54% | NOISE (no measurable edge) |
| 1 to 3 days | 292 | +0.10c | +0.33c | 55% | NOISE (no measurable edge) |
| over a month | 3393 | -0.07c | -0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1263 | -0.48c | +0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 82 | +1.87c | 55% |
| p_6h (alerted only) | 71 | +2.72c | 52% |
| p_24h (alerted only) | 44 | +3.41c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

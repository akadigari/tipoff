# What the scanner has learned about itself

_Auto-generated 2026-08-20T15:43:14Z. 10000 candidates logged, 5180 with a filled 24h forward price._

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
| alerted (passed gate and score) | 33 | +0.31c | +0.00c | 50% | NOISE (no measurable edge) |
| filtered out | 4980 | -0.16c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 167 | -0.66c | -0.00c | 54% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 8 | +0.84c | +0.55c | 86% | INSUFFICIENT DATA |
| cross_platform | 122 | +0.75c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 696 | +0.36c | +0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4557 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 205 | -0.19c | -0.55c | 45% | NOISE (no measurable edge) |
| thin_market | 46 | -0.19c | +0.08c | 64% | NOISE (no measurable edge) |
| large_trade | 1529 | -0.22c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1099 | -0.34c | +0.05c | 56% | NOISE (no measurable edge) |
| insiderable | 465 | -0.40c | -0.00c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.45c | +0.05c | 57% | INSUFFICIENT DATA |
| price_jump | 699 | -1.47c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 684 | +0.31c | +0.05c | 56% | NOISE (no measurable edge) |
| politics | 2428 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 1957 | -0.43c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 111 | -1.83c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3309 | -0.09c | -0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 481 | -0.09c | -0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 667 | -0.31c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 723 | -0.47c | +0.00c | 55% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4715 | -0.15c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 465 | -0.40c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 55 | +4.49c | +0.00c | 51% | FOLLOW |
| over a month | 3369 | -0.17c | -0.00c | 46% | NOISE (no measurable edge) |
| 3 to 7 days | 238 | -0.32c | +0.25c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1124 | -0.38c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 259 | -0.99c | +0.10c | 53% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 81 | +1.90c | 57% |
| p_6h (alerted only) | 66 | +3.08c | 57% |
| p_24h (alerted only) | 33 | +0.31c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

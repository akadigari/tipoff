# What the scanner has learned about itself

_Auto-generated 2026-08-19T13:52:04Z. 10000 candidates logged, 5381 with a filled 24h forward price._

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
| alerted (passed gate and score) | 38 | -0.01c | +0.22c | 53% | NOISE (no measurable edge) |
| filtered out | 5163 | -0.15c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 180 | -1.06c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| within_trader | 730 | +0.32c | +0.00c | 56% | NOISE (no measurable edge) |
| cross_platform | 129 | +0.08c | +0.00c | 48% | NOISE (no measurable edge) |
| thin_market | 51 | +0.03c | +0.05c | 63% | NOISE (no measurable edge) |
| price_impact | 210 | +0.03c | -0.60c | 45% | NOISE (no measurable edge) |
| coordination | 8 | +0.02c | +0.40c | 71% | INSUFFICIENT DATA |
| repeat_actor | 1193 | -0.06c | -0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4743 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1677 | -0.07c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 28 | -0.22c | +0.02c | 54% | INSUFFICIENT DATA |
| insiderable | 495 | -0.33c | +0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 735 | -1.23c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 681 | +0.27c | -0.00c | 54% | NOISE (no measurable edge) |
| politics | 2469 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2115 | -0.27c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 107 | -1.90c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 9 | -3.94c | -1.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 770 | -0.07c | +0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3346 | -0.14c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 521 | -0.18c | +0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 744 | -0.47c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4886 | -0.16c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 495 | -0.33c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 71 | +1.00c | +0.00c | 46% | NOISE (no measurable edge) |
| 3 to 7 days | 301 | -0.06c | +0.00c | 51% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1194 | -0.07c | -0.00c | 50% | NOISE (no measurable edge) |
| over a month | 3413 | -0.14c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 269 | -1.38c | -0.00c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 67 | +0.10c | 51% |
| p_6h (alerted only) | 59 | +0.32c | 50% |
| p_24h (alerted only) | 38 | -0.01c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

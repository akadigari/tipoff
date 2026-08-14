# What the scanner has learned about itself

_Auto-generated 2026-08-14T23:31:07Z. 10000 candidates logged, 5565 with a filled 24h forward price._

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
| alerted (passed gate and score) | 71 | +1.18c | +1.00c | 54% | FOLLOW |
| filtered out | 5283 | +0.22c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 211 | -1.15c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 68 | +1.66c | +0.47c | 67% | FOLLOW |
| cross_platform | 164 | +1.43c | +0.00c | 53% | FOLLOW |
| repeat_actor | 1285 | +0.88c | +0.15c | 59% | NOISE (no measurable edge) |
| within_trader | 751 | +0.88c | +0.10c | 60% | NOISE (no measurable edge) |
| large_trade | 1843 | +0.77c | +0.10c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 25 | +0.59c | -0.00c | 52% | INSUFFICIENT DATA |
| volume_spike | 4794 | +0.26c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 488 | +0.13c | +0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 884 | -0.10c | -0.00c | 51% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 258 | -0.83c | -0.65c | 45% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 560 | +0.33c | +0.00c | 52% | NOISE (no measurable edge) |
| politics | 2421 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2437 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 127 | -0.29c | -0.40c | 42% | NOISE (no measurable edge) |
| sports | 20 | -4.63c | -3.25c | 32% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 818 | +0.77c | +0.08c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 803 | +0.38c | +0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 562 | +0.32c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3382 | -0.04c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5077 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| high | 488 | +0.13c | +0.00c | 54% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 66 | +1.82c | +1.13c | 59% | FOLLOW |
| 3 to 7 days | 412 | +1.52c | +0.30c | 57% | FOLLOW |
| 1 to 4 weeks | 1280 | +0.48c | +0.02c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 321 | +0.37c | +0.30c | 55% | NOISE (no measurable edge) |
| over a month | 3385 | -0.08c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 102 | -0.23c | 44% |
| p_6h (alerted only) | 97 | -0.31c | 44% |
| p_24h (alerted only) | 71 | +1.18c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

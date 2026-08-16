# What the scanner has learned about itself

_Auto-generated 2026-08-16T23:29:38Z. 10000 candidates logged, 5784 with a filled 24h forward price._

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
| alerted (passed gate and score) | 63 | +0.89c | +0.45c | 52% | NOISE (no measurable edge) |
| filtered out | 5503 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 218 | -0.74c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 144 | +1.21c | +0.00c | 53% | FOLLOW |
| thin_market | 77 | +1.04c | +0.30c | 68% | FOLLOW |
| within_trader | 810 | +0.93c | +0.10c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1317 | +0.73c | +0.10c | 59% | NOISE (no measurable edge) |
| large_trade | 1872 | +0.66c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 5032 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 529 | +0.04c | -0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 28 | -0.35c | -0.03c | 44% | INSUFFICIENT DATA |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_jump | 874 | -0.56c | -0.10c | 48% | NOISE (no measurable edge) |
| price_impact | 251 | -0.71c | -0.65c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 624 | +0.30c | +0.00c | 53% | NOISE (no measurable edge) |
| politics | 2599 | +0.10c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2407 | +0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 138 | -0.99c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 16 | -2.78c | -0.75c | 40% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 836 | +0.63c | +0.05c | 57% | NOISE (no measurable edge) |
| 70+ | 588 | +0.35c | -0.00c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 800 | +0.12c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3560 | -0.12c | +0.00c | 46% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5255 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 529 | +0.04c | -0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 73 | +1.52c | +0.40c | 54% | FOLLOW |
| 3 to 7 days | 428 | +0.83c | +0.20c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 364 | +0.47c | +0.10c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1283 | +0.37c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3508 | -0.15c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 89 | +0.22c | 52% |
| p_6h (alerted only) | 84 | +0.29c | 46% |
| p_24h (alerted only) | 63 | +0.89c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

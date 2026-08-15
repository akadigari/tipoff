# What the scanner has learned about itself

_Auto-generated 2026-08-15T01:44:55Z. 10000 candidates logged, 5558 with a filled 24h forward price._

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
| alerted (passed gate and score) | 71 | +0.98c | +1.00c | 54% | NOISE (no measurable edge) |
| filtered out | 5275 | +0.21c | -0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 212 | -1.14c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 69 | +1.65c | +0.50c | 68% | FOLLOW |
| cross_platform | 161 | +1.37c | +0.00c | 52% | FOLLOW |
| within_trader | 754 | +0.88c | +0.10c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1281 | +0.86c | +0.15c | 59% | NOISE (no measurable edge) |
| large_trade | 1838 | +0.76c | +0.10c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 25 | +0.59c | -0.00c | 52% | INSUFFICIENT DATA |
| volume_spike | 4784 | +0.26c | +0.00c | 52% | NOISE (no measurable edge) |
| insiderable | 487 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 891 | -0.15c | -0.00c | 51% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 256 | -0.84c | -0.65c | 45% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 556 | +0.34c | +0.00c | 53% | NOISE (no measurable edge) |
| politics | 2428 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2428 | +0.15c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 126 | -0.29c | -0.25c | 42% | NOISE (no measurable edge) |
| sports | 20 | -4.63c | -3.25c | 32% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 814 | +0.77c | +0.10c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 800 | +0.38c | +0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 565 | +0.27c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3379 | -0.05c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5071 | +0.17c | -0.00c | 51% | NOISE (no measurable edge) |
| high | 487 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 63 | +1.70c | +1.00c | 57% | FOLLOW |
| 3 to 7 days | 413 | +1.49c | +0.30c | 57% | FOLLOW |
| 1 to 4 weeks | 1272 | +0.48c | +0.05c | 54% | NOISE (no measurable edge) |
| 1 to 3 days | 323 | +0.27c | +0.30c | 54% | NOISE (no measurable edge) |
| over a month | 3386 | -0.08c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 101 | -0.20c | 44% |
| p_6h (alerted only) | 96 | -0.25c | 44% |
| p_24h (alerted only) | 71 | +0.98c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

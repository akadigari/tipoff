# What the scanner has learned about itself

_Auto-generated 2026-08-14T16:00:26Z. 10000 candidates logged, 5523 with a filled 24h forward price._

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
| alerted (passed gate and score) | 76 | +0.43c | +0.50c | 51% | NOISE (no measurable edge) |
| filtered out | 5232 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 215 | -0.99c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 69 | +1.65c | +0.45c | 68% | FOLLOW |
| cross_platform | 158 | +1.54c | +0.00c | 54% | FOLLOW |
| within_trader | 763 | +0.79c | +0.10c | 59% | NOISE (no measurable edge) |
| repeat_actor | 1299 | +0.76c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1850 | +0.66c | +0.08c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 22 | +0.61c | -0.03c | 45% | INSUFFICIENT DATA |
| volume_spike | 4776 | +0.22c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 473 | +0.14c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 854 | -0.18c | -0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 252 | -0.49c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 556 | +0.24c | +0.00c | 52% | NOISE (no measurable edge) |
| politics | 2385 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2437 | +0.09c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 123 | +0.09c | -0.00c | 42% | NOISE (no measurable edge) |
| sports | 22 | -4.43c | -3.00c | 29% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 829 | +0.60c | +0.05c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 777 | +0.46c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 559 | +0.28c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3358 | -0.08c | +0.00c | 48% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 473 | +0.14c | +0.00c | 53% | NOISE (no measurable edge) |
| normal | 5050 | +0.13c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 65 | +1.64c | +1.00c | 58% | FOLLOW |
| 3 to 7 days | 392 | +1.62c | +0.40c | 59% | FOLLOW |
| 1 to 4 weeks | 1297 | +0.40c | +0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 316 | -0.02c | +0.28c | 54% | NOISE (no measurable edge) |
| over a month | 3356 | -0.10c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 107 | +0.15c | 44% |
| p_6h (alerted only) | 103 | -0.25c | 45% |
| p_24h (alerted only) | 76 | +0.43c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

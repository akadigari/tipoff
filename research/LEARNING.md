# What the scanner has learned about itself

_Auto-generated 2026-08-16T16:36:36Z. 10000 candidates logged, 5776 with a filled 24h forward price._

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
| alerted (passed gate and score) | 67 | +0.72c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5493 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 216 | -0.82c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 148 | +1.16c | +0.00c | 53% | FOLLOW |
| thin_market | 71 | +1.08c | +0.30c | 69% | FOLLOW |
| within_trader | 797 | +1.03c | +0.10c | 60% | FOLLOW |
| repeat_actor | 1309 | +0.77c | +0.10c | 59% | NOISE (no measurable edge) |
| large_trade | 1866 | +0.70c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 5009 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 518 | +0.03c | +0.00c | 53% | NOISE (no measurable edge) |
| price_impact | 256 | -0.39c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_jump | 890 | -0.54c | -0.10c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 29 | -1.00c | -0.05c | 42% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 620 | +0.33c | +0.00c | 54% | NOISE (no measurable edge) |
| other | 2411 | +0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2596 | +0.06c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 131 | -0.21c | +0.00c | 45% | NOISE (no measurable edge) |
| sports | 18 | -4.58c | -1.50c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 830 | +0.77c | +0.10c | 58% | NOISE (no measurable edge) |
| 70+ | 588 | +0.25c | -0.00c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 796 | +0.18c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3562 | -0.10c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5258 | +0.11c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 518 | +0.03c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 70 | +1.60c | +0.67c | 54% | FOLLOW |
| 3 to 7 days | 430 | +1.25c | +0.23c | 56% | FOLLOW |
| 1 to 4 weeks | 1290 | +0.49c | +0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 351 | +0.34c | +0.10c | 55% | NOISE (no measurable edge) |
| over a month | 3512 | -0.18c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +0.02c | 49% |
| p_6h (alerted only) | 88 | +0.15c | 45% |
| p_24h (alerted only) | 67 | +0.72c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

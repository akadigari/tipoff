# What the scanner has learned about itself

_Auto-generated 2026-08-14T02:37:04Z. 10000 candidates logged, 5642 with a filled 24h forward price._

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
| alerted (passed gate and score) | 77 | +0.85c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5343 | +0.21c | -0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 222 | -0.90c | -0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 67 | +1.70c | +0.50c | 67% | FOLLOW |
| cross_platform | 158 | +1.56c | +0.00c | 55% | FOLLOW |
| chatter | 2 | +1.00c | +1.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 24 | +0.73c | -0.03c | 43% | INSUFFICIENT DATA |
| repeat_actor | 1332 | +0.68c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1893 | +0.65c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 789 | +0.60c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4851 | +0.21c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 495 | +0.10c | -0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 894 | +0.04c | -0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 263 | -0.22c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 4 | -1.26c | -0.03c | 33% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2533 | +0.26c | -0.00c | 51% | NOISE (no measurable edge) |
| politics | 2413 | +0.24c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 545 | -0.04c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 127 | -0.94c | +0.00c | 45% | NOISE (no measurable edge) |
| sports | 24 | -4.60c | -3.50c | 26% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 841 | +0.60c | +0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 802 | +0.46c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 574 | +0.20c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3425 | -0.00c | -0.00c | 48% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5147 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| high | 495 | +0.10c | -0.00c | 52% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 395 | +1.62c | +0.35c | 58% | FOLLOW |
| 1 to 4 weeks | 1346 | +0.39c | +0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 326 | +0.31c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3408 | -0.04c | +0.00c | 48% | NOISE (no measurable edge) |
| under 1 day | 69 | -1.08c | +0.40c | 55% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 108 | +0.19c | 45% |
| p_6h (alerted only) | 101 | -0.34c | 44% |
| p_24h (alerted only) | 77 | +0.85c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

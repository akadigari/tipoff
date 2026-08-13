# What the scanner has learned about itself

_Auto-generated 2026-08-13T22:55:17Z. 10000 candidates logged, 5734 with a filled 24h forward price._

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
| alerted (passed gate and score) | 79 | +0.77c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5425 | +0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 230 | -0.91c | +0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 6 | +14.81c | +14.63c | 100% | INSUFFICIENT DATA |
| thin_market | 68 | +1.68c | +0.47c | 67% | FOLLOW |
| cross_platform | 160 | +1.52c | +0.00c | 53% | FOLLOW |
| repeat_actor | 1377 | +0.85c | +0.10c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 24 | +0.73c | -0.03c | 43% | INSUFFICIENT DATA |
| large_trade | 1948 | +0.72c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 808 | +0.65c | +0.05c | 58% | NOISE (no measurable edge) |
| insiderable | 510 | +0.27c | -0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4937 | +0.24c | +0.00c | 51% | NOISE (no measurable edge) |
| price_jump | 904 | +0.16c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 266 | -0.26c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 5 | -1.29c | -0.05c | 25% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2442 | +0.31c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2585 | +0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 551 | +0.02c | -0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 130 | -0.99c | +0.00c | 44% | NOISE (no measurable edge) |
| sports | 26 | -4.88c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 862 | +0.63c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 815 | +0.48c | -0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 593 | +0.44c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3464 | -0.02c | +0.00c | 48% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 510 | +0.27c | -0.00c | 52% | NOISE (no measurable edge) |
| normal | 5224 | +0.19c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 396 | +1.62c | +0.33c | 58% | FOLLOW |
| 1 to 4 weeks | 1368 | +0.49c | -0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 332 | +0.40c | +0.18c | 54% | NOISE (no measurable edge) |
| over a month | 3467 | -0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| under 1 day | 69 | -1.54c | +0.40c | 55% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 107 | +0.16c | 46% |
| p_6h (alerted only) | 102 | -0.35c | 44% |
| p_24h (alerted only) | 79 | +0.77c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

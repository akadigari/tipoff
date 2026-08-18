# What the scanner has learned about itself

_Auto-generated 2026-08-18T04:45:09Z. 10000 candidates logged, 5582 with a filled 24h forward price._

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
| filtered out | 5328 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 51 | -0.16c | -0.15c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 203 | -0.54c | +0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 137 | +1.27c | -0.00c | 52% | FOLLOW |
| thin_market | 87 | +0.92c | +0.30c | 67% | NOISE (no measurable edge) |
| within_trader | 774 | +0.79c | +0.10c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1277 | +0.50c | +0.10c | 58% | NOISE (no measurable edge) |
| price_impact | 231 | +0.49c | -0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1812 | +0.48c | +0.00c | 57% | NOISE (no measurable edge) |
| volume_spike | 4886 | +0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| coordination | 8 | +0.04c | +0.40c | 71% | INSUFFICIENT DATA |
| insiderable | 508 | -0.16c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.27c | -0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 809 | -0.73c | -0.50c | 48% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 629 | +0.21c | +0.00c | 53% | NOISE (no measurable edge) |
| politics | 2564 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2251 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 124 | -0.64c | +0.00c | 50% | NOISE (no measurable edge) |
| sports | 14 | -3.50c | -0.75c | 38% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 821 | +0.41c | +0.00c | 56% | NOISE (no measurable edge) |
| 70+ | 556 | +0.19c | -0.00c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 766 | +0.07c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3439 | -0.02c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5074 | +0.10c | -0.00c | 50% | NOISE (no measurable edge) |
| high | 508 | -0.16c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 79 | +1.34c | +0.20c | 53% | FOLLOW |
| 3 to 7 days | 385 | +0.99c | +0.25c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1221 | +0.46c | +0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3410 | -0.08c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 350 | -0.53c | +0.05c | 53% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 74 | +0.02c | 48% |
| p_6h (alerted only) | 69 | -0.26c | 45% |
| p_24h (alerted only) | 51 | -0.16c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

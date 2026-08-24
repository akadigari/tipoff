# What the scanner has learned about itself

_Auto-generated 2026-08-24T05:48:29Z. 10000 candidates logged, 5773 with a filled 24h forward price._

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
| alerted (passed gate and score) | 57 | -0.01c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5511 | -0.06c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 205 | -1.15c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 89 | +1.14c | -0.00c | 53% | FOLLOW |
| price_impact | 277 | +1.00c | -0.10c | 49% | FOLLOW |
| volume_spike | 5106 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 851 | -0.14c | +0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 532 | -0.20c | +0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.36c | -0.00c | 43% | INSUFFICIENT DATA |
| price_jump | 786 | -0.43c | -0.38c | 49% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1863 | -0.61c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1373 | -0.70c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 44 | -1.78c | +0.03c | 55% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1270 | +0.26c | +0.05c | 53% | NOISE (no measurable edge) |
| politics | 2133 | +0.14c | -0.00c | 51% | NOISE (no measurable edge) |
| other | 2267 | -0.43c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 103 | -2.29c | +0.00c | 45% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3514 | +0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 742 | +0.04c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 624 | -0.33c | +0.00c | 55% | NOISE (no measurable edge) |
| 55 to 69 | 893 | -0.80c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5241 | -0.09c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 532 | -0.20c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 44 | +4.28c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 237 | +0.71c | +0.40c | 54% | NOISE (no measurable edge) |
| over a month | 3589 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 307 | -0.39c | +0.15c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1464 | -0.60c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 95 | +1.34c | 59% |
| p_6h (alerted only) | 84 | +1.77c | 51% |
| p_24h (alerted only) | 57 | -0.01c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

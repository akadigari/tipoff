# What the scanner has learned about itself

_Auto-generated 2026-08-22T22:32:32Z. 10000 candidates logged, 5654 with a filled 24h forward price._

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
| alerted (passed gate and score) | 45 | +3.29c | +1.00c | 57% | FOLLOW |
| filtered out | 5416 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 193 | -0.97c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 246 | +1.88c | +0.50c | 53% | FOLLOW |
| cross_platform | 95 | +1.06c | +0.00c | 52% | FOLLOW |
| price_jump | 741 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 5023 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 780 | -0.22c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 491 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1731 | -0.63c | +0.00c | 52% | NOISE (no measurable edge) |
| thin_market | 42 | -0.72c | +0.08c | 61% | NOISE (no measurable edge) |
| repeat_actor | 1263 | -0.79c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 21 | -1.03c | -0.00c | 44% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1129 | +0.61c | +0.15c | 55% | NOISE (no measurable edge) |
| politics | 2202 | +0.09c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2236 | -0.39c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 87 | -1.41c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 715 | +0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3550 | +0.16c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 562 | -0.32c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 827 | -0.74c | -0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5163 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 491 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +5.26c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 245 | +0.98c | +0.25c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 290 | +0.50c | +0.40c | 56% | NOISE (no measurable edge) |
| over a month | 3557 | +0.01c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1364 | -0.65c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 86 | +1.47c | 56% |
| p_6h (alerted only) | 75 | +2.85c | 51% |
| p_24h (alerted only) | 45 | +3.29c | 57% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

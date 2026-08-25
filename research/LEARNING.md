# What the scanner has learned about itself

_Auto-generated 2026-08-25T08:59:16Z. 10000 candidates logged, 5656 with a filled 24h forward price._

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
| filtered out | 5394 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 207 | -0.81c | +0.00c | 52% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 55 | -0.99c | -0.50c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 78 | +1.07c | +0.00c | 45% | FOLLOW |
| price_impact | 294 | +0.87c | -0.50c | 48% | NOISE (no measurable edge) |
| volume_spike | 4988 | -0.01c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 837 | -0.01c | -0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 527 | -0.05c | +0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 15 | -0.27c | -0.05c | 38% | INSUFFICIENT DATA |
| price_jump | 774 | -0.35c | -0.05c | 49% | NOISE (no measurable edge) |
| large_trade | 1844 | -0.52c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1371 | -0.61c | +0.00c | 54% | NOISE (no measurable edge) |
| coordination | 7 | -0.63c | +0.60c | 83% | INSUFFICIENT DATA |
| thin_market | 34 | -2.76c | +0.03c | 52% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1329 | +0.33c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2032 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2202 | -0.32c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 93 | -0.84c | -0.00c | 42% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 736 | +0.26c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3420 | +0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 641 | -0.40c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 859 | -0.59c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5129 | -0.05c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 527 | -0.05c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 37 | +4.93c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 224 | +1.57c | +0.30c | 54% | FOLLOW |
| over a month | 3506 | +0.02c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 250 | -0.15c | +0.50c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1523 | -0.62c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 96 | +0.97c | 54% |
| p_6h (alerted only) | 81 | +2.35c | 51% |
| p_24h (alerted only) | 55 | -0.99c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

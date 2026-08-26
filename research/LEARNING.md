# What the scanner has learned about itself

_Auto-generated 2026-08-26T19:14:52Z. 10000 candidates logged, 5852 with a filled 24h forward price._

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
| alerted (passed gate and score) | 61 | +0.34c | -0.50c | 47% | NOISE (no measurable edge) |
| filtered out | 5584 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 207 | -1.20c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 55 | +1.38c | -0.00c | 44% | FOLLOW |
| price_impact | 320 | +0.18c | -0.68c | 47% | NOISE (no measurable edge) |
| insiderable | 513 | +0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 5119 | -0.01c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 846 | -0.17c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.38c | -0.05c | 31% | INSUFFICIENT DATA |
| large_trade | 1960 | -0.42c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1444 | -0.55c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 850 | -0.84c | -0.18c | 49% | NOISE (no measurable edge) |
| coordination | 8 | -1.09c | +0.03c | 50% | INSUFFICIENT DATA |
| chatter | 2 | -1.75c | -1.75c | 0% | INSUFFICIENT DATA |
| thin_market | 30 | -3.27c | +0.08c | 55% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1468 | +0.16c | +0.05c | 52% | NOISE (no measurable edge) |
| politics | 2023 | +0.00c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2266 | -0.26c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 95 | -1.07c | -1.00c | 35% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 745 | +0.26c | +0.00c | 50% | NOISE (no measurable edge) |
| under 40 | 3524 | +0.08c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 930 | -0.55c | +0.00c | 52% | NOISE (no measurable edge) |
| 70+ | 653 | -0.63c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 513 | +0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| normal | 5339 | -0.10c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 385 | +1.16c | +0.35c | 56% | FOLLOW |
| over a month | 3599 | -0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 269 | -0.51c | +0.70c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1483 | -0.68c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | +1.11c | 54% |
| p_6h (alerted only) | 82 | +2.73c | 54% |
| p_24h (alerted only) | 61 | +0.34c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-25T23:33:23Z. 10000 candidates logged, 5617 with a filled 24h forward price._

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
| filtered out | 5350 | -0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 57 | -0.24c | -0.50c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 210 | -1.09c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 65 | +1.18c | +0.00c | 44% | FOLLOW |
| price_impact | 302 | +0.11c | -1.00c | 47% | NOISE (no measurable edge) |
| insiderable | 504 | -0.01c | +0.00c | 47% | NOISE (no measurable edge) |
| volume_spike | 4937 | -0.04c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 825 | -0.11c | -0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 14 | -0.39c | -0.03c | 36% | INSUFFICIENT DATA |
| price_jump | 787 | -0.46c | +0.00c | 50% | NOISE (no measurable edge) |
| large_trade | 1855 | -0.47c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1368 | -0.60c | +0.00c | 53% | NOISE (no measurable edge) |
| coordination | 8 | -0.99c | +0.13c | 57% | INSUFFICIENT DATA |
| thin_market | 33 | -2.89c | -0.00c | 50% | FADE (signal points the wrong way) |
| chatter | 1 | -3.50c | -3.50c | 0% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1354 | +0.10c | +0.05c | 52% | NOISE (no measurable edge) |
| politics | 1987 | -0.02c | -0.00c | 49% | NOISE (no measurable edge) |
| other | 2181 | -0.19c | -0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 95 | -0.98c | -0.50c | 38% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 733 | +0.22c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3383 | +0.08c | -0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 877 | -0.51c | -0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 624 | -0.63c | +0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 504 | -0.01c | +0.00c | 47% | NOISE (no measurable edge) |
| normal | 5113 | -0.08c | -0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 23 | +7.54c | +0.55c | 55% | INSUFFICIENT DATA |
| 3 to 7 days | 228 | +1.16c | +0.00c | 50% | FOLLOW |
| over a month | 3494 | +0.02c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 247 | -0.16c | +0.55c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1517 | -0.68c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | +1.03c | 55% |
| p_6h (alerted only) | 83 | +2.78c | 54% |
| p_24h (alerted only) | 57 | -0.24c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

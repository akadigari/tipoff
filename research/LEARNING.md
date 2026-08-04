# What the scanner has learned about itself

_Auto-generated 2026-08-04T17:59:57Z. 10000 candidates logged, 5800 with a filled 24h forward price._

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
| alerted (passed gate and score) | 73 | -0.33c | -1.00c | 45% | NOISE (no measurable edge) |
| filtered out | 5494 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 233 | -0.54c | -0.00c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 17 | +2.48c | +0.15c | 56% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4787 | -0.27c | -0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2046 | -0.35c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1420 | -0.37c | +0.00c | 54% | NOISE (no measurable edge) |
| cross_platform | 115 | -0.50c | -0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 282 | -0.57c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 610 | -0.62c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 857 | -0.71c | +0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 1190 | -1.00c | -1.00c | 46% | NOISE (no measurable edge) |
| thin_market | 43 | -1.43c | +0.00c | 44% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 532 | +0.20c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2282 | -0.18c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 370 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2593 | -0.68c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 23 | -1.57c | -1.00c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 872 | -0.25c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3456 | -0.27c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 813 | -0.57c | -0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 659 | -0.91c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5190 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 610 | -0.62c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 552 | +0.41c | +0.33c | 53% | NOISE (no measurable edge) |
| over a month | 3768 | -0.29c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 951 | -0.53c | -0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 396 | -1.94c | -0.30c | 47% | FADE (signal points the wrong way) |
| under 1 day | 35 | -2.60c | +0.05c | 55% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 100 | +0.40c | 41% |
| p_6h (alerted only) | 90 | -1.03c | 44% |
| p_24h (alerted only) | 73 | -0.33c | 45% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

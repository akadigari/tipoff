# What the scanner has learned about itself

_Auto-generated 2026-08-06T15:23:32Z. 10000 candidates logged, 5907 with a filled 24h forward price._

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
| filtered out | 5594 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 235 | -0.60c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 78 | -0.79c | -0.60c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| fresh_wallet | 19 | +0.59c | +0.15c | 56% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| cross_platform | 135 | -0.08c | -0.00c | 46% | NOISE (no measurable edge) |
| volume_spike | 4910 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2062 | -0.36c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1424 | -0.38c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 596 | -0.61c | -0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1167 | -0.82c | -0.50c | 48% | NOISE (no measurable edge) |
| thin_market | 44 | -1.01c | -0.00c | 49% | FADE (signal points the wrong way) |
| within_trader | 859 | -1.03c | +0.00c | 53% | FADE (signal points the wrong way) |
| price_impact | 287 | -1.15c | -0.85c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 525 | +0.16c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2375 | -0.13c | -0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 366 | -0.39c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2622 | -0.69c | -0.00c | 48% | NOISE (no measurable edge) |
| sports | 19 | -3.26c | -3.00c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3535 | -0.28c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 887 | -0.29c | -0.00c | 53% | NOISE (no measurable edge) |
| 40 to 54 | 844 | -0.37c | -0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 641 | -1.05c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5311 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 596 | -0.61c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 555 | +0.44c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3897 | -0.24c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 930 | -0.41c | +0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 388 | -2.64c | -0.33c | 48% | FADE (signal points the wrong way) |
| under 1 day | 39 | -4.03c | +0.05c | 54% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 106 | +0.40c | 44% |
| p_6h (alerted only) | 99 | -0.92c | 45% |
| p_24h (alerted only) | 78 | -0.79c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

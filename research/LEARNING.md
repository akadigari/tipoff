# What the scanner has learned about itself

_Auto-generated 2026-08-09T08:55:58Z. 10000 candidates logged, 5812 with a filled 24h forward price._

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
| alerted (passed gate and score) | 81 | +0.92c | +1.00c | 54% | NOISE (no measurable edge) |
| filtered out | 5490 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 241 | -0.87c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 153 | +0.28c | +0.00c | 51% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| fresh_wallet | 20 | +0.02c | +0.07c | 53% | INSUFFICIENT DATA |
| large_trade | 1985 | -0.22c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4870 | -0.25c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 527 | -0.29c | -0.00c | 45% | NOISE (no measurable edge) |
| repeat_actor | 1366 | -0.29c | +0.00c | 55% | NOISE (no measurable edge) |
| coordination | 2 | -0.37c | -0.37c | 50% | INSUFFICIENT DATA |
| thin_market | 45 | -0.44c | -0.00c | 55% | NOISE (no measurable edge) |
| price_jump | 1064 | -0.65c | -1.00c | 47% | NOISE (no measurable edge) |
| within_trader | 863 | -0.85c | +0.00c | 54% | NOISE (no measurable edge) |
| price_impact | 282 | -1.14c | -1.00c | 44% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2358 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 525 | -0.15c | -0.00c | 47% | NOISE (no measurable edge) |
| other | 2605 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 307 | -0.70c | -0.15c | 44% | NOISE (no measurable edge) |
| sports | 17 | -5.97c | -5.50c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 808 | -0.02c | +0.00c | 51% | NOISE (no measurable edge) |
| 55 to 69 | 863 | -0.10c | +0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3530 | -0.38c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 611 | -1.07c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 527 | -0.29c | -0.00c | 45% | NOISE (no measurable edge) |
| normal | 5285 | -0.37c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 513 | +0.05c | -0.00c | 50% | NOISE (no measurable edge) |
| over a month | 3820 | -0.24c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 948 | -0.37c | +0.00c | 51% | NOISE (no measurable edge) |
| 1 to 3 days | 407 | -2.09c | -0.20c | 48% | FADE (signal points the wrong way) |
| under 1 day | 38 | -4.68c | +0.13c | 56% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.60c | 47% |
| p_6h (alerted only) | 110 | -0.67c | 46% |
| p_24h (alerted only) | 81 | +0.92c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

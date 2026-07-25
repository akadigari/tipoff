# What the scanner has learned about itself

_Auto-generated 2026-07-25T18:03:44Z. 10000 candidates logged, 5951 with a filled 24h forward price._

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
| filtered out | 5628 | -0.48c | +0.00c | 47% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 99 | -1.64c | -1.00c | 41% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 224 | -1.91c | +0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 4 | +1.52c | +1.55c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1108 | -0.15c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 773 | -0.19c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1805 | -0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4793 | -0.33c | -0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 347 | -0.94c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 612 | -0.97c | -0.00c | 46% | NOISE (no measurable edge) |
| thin_market | 24 | -1.38c | -0.50c | 38% | INSUFFICIENT DATA |
| price_jump | 1384 | -1.97c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 90 | -2.04c | +0.00c | 42% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 61 | +0.57c | +0.30c | 59% | NOISE (no measurable edge) |
| politics | 2075 | -0.48c | +0.00c | 44% | NOISE (no measurable edge) |
| other | 2815 | -0.54c | -0.00c | 48% | NOISE (no measurable edge) |
| crypto | 655 | -0.64c | -0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 345 | -1.19c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3693 | -0.44c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 797 | -0.55c | -0.00c | 48% | NOISE (no measurable edge) |
| 40 to 54 | 873 | -0.67c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 588 | -1.10c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5339 | -0.51c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 612 | -0.97c | -0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 20 | +3.03c | -0.20c | 50% | INSUFFICIENT DATA |
| 3 to 7 days | 244 | +0.67c | +0.75c | 57% | NOISE (no measurable edge) |
| 1 to 3 days | 213 | -0.47c | -0.30c | 49% | NOISE (no measurable edge) |
| over a month | 3548 | -0.49c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1838 | -0.93c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 135 | -0.90c | 44% |
| p_6h (alerted only) | 125 | -1.30c | 46% |
| p_24h (alerted only) | 99 | -1.64c | 41% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

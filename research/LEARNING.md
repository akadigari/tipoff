# What the scanner has learned about itself

_Auto-generated 2026-08-23T06:55:48Z. 10000 candidates logged, 5771 with a filled 24h forward price._

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
| alerted (passed gate and score) | 49 | +2.28c | +1.00c | 58% | FOLLOW |
| filtered out | 5525 | -0.02c | -0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 197 | -0.94c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 273 | +1.14c | -0.10c | 48% | FOLLOW |
| cross_platform | 93 | +1.07c | +0.00c | 51% | FOLLOW |
| volume_spike | 5114 | -0.07c | -0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 776 | -0.12c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 820 | -0.17c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 510 | -0.29c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1793 | -0.60c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1325 | -0.72c | -0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 44 | -0.76c | +0.05c | 57% | NOISE (no measurable edge) |
| fresh_wallet | 20 | -1.08c | +0.00c | 47% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1219 | +0.49c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2184 | +0.11c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2277 | -0.36c | -0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 91 | -2.05c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3590 | +0.16c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 724 | +0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 602 | -0.38c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 855 | -0.75c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5261 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 510 | -0.29c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +5.26c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 255 | +0.97c | +0.25c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 295 | +0.17c | +0.35c | 56% | NOISE (no measurable edge) |
| over a month | 3597 | -0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1427 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 91 | +1.40c | 57% |
| p_6h (alerted only) | 78 | +2.46c | 51% |
| p_24h (alerted only) | 49 | +2.28c | 58% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

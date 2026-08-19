# What the scanner has learned about itself

_Auto-generated 2026-08-19T22:35:29Z. 10000 candidates logged, 5211 with a filled 24h forward price._

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
| alerted (passed gate and score) | 40 | +0.10c | +0.22c | 53% | NOISE (no measurable edge) |
| filtered out | 5000 | -0.12c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 171 | -1.08c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 118 | +0.74c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 706 | +0.41c | +0.00c | 55% | NOISE (no measurable edge) |
| price_impact | 207 | +0.29c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 9 | +0.08c | +0.50c | 75% | INSUFFICIENT DATA |
| volume_spike | 4587 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| thin_market | 47 | -0.09c | +0.05c | 62% | NOISE (no measurable edge) |
| large_trade | 1592 | -0.15c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1141 | -0.20c | -0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 486 | -0.28c | +0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 26 | -0.34c | +0.02c | 55% | INSUFFICIENT DATA |
| price_jump | 715 | -1.47c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 693 | +0.55c | +0.05c | 55% | NOISE (no measurable edge) |
| politics | 2389 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2016 | -0.39c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 109 | -1.93c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 4 | -3.75c | -2.25c | 50% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 701 | -0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3274 | -0.13c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 490 | -0.25c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 746 | -0.26c | +0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4725 | -0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 486 | -0.28c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 62 | +4.72c | +0.00c | 52% | FOLLOW |
| over a month | 3326 | -0.13c | +0.00c | 47% | NOISE (no measurable edge) |
| 3 to 7 days | 280 | -0.21c | +0.10c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1141 | -0.28c | -0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 267 | -0.77c | +0.05c | 51% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 82 | +1.60c | 55% |
| p_6h (alerted only) | 61 | +1.37c | 54% |
| p_24h (alerted only) | 40 | +0.10c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

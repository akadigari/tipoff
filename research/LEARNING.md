# What the scanner has learned about itself

_Auto-generated 2026-08-20T07:00:30Z. 10000 candidates logged, 5255 with a filled 24h forward price._

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
| alerted (passed gate and score) | 37 | -0.00c | +0.45c | 53% | NOISE (no measurable edge) |
| filtered out | 5052 | -0.26c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 166 | -0.71c | +0.00c | 53% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 120 | +0.57c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 698 | +0.36c | +0.00c | 56% | NOISE (no measurable edge) |
| coordination | 9 | +0.08c | +0.50c | 75% | INSUFFICIENT DATA |
| volume_spike | 4601 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1574 | -0.09c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1129 | -0.15c | +0.05c | 56% | NOISE (no measurable edge) |
| thin_market | 46 | -0.19c | +0.08c | 64% | NOISE (no measurable edge) |
| fresh_wallet | 24 | -0.43c | +0.02c | 52% | INSUFFICIENT DATA |
| insiderable | 473 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 213 | -0.89c | -1.00c | 44% | NOISE (no measurable edge) |
| price_jump | 730 | -1.89c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2449 | -0.03c | -0.00c | 50% | NOISE (no measurable edge) |
| crypto | 699 | -0.19c | +0.00c | 54% | NOISE (no measurable edge) |
| other | 1992 | -0.51c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 113 | -1.76c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 2 | -5.25c | -5.25c | 50% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 477 | -0.17c | -0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3342 | -0.26c | +0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 743 | -0.28c | -0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 693 | -0.38c | -0.00c | 49% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4782 | -0.25c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 473 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 57 | +4.63c | +0.00c | 51% | FOLLOW |
| over a month | 3395 | -0.25c | -0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1141 | -0.43c | -0.00c | 49% | NOISE (no measurable edge) |
| 3 to 7 days | 266 | -0.57c | +0.23c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 262 | -1.77c | +0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 82 | +1.86c | 55% |
| p_6h (alerted only) | 69 | +2.41c | 54% |
| p_24h (alerted only) | 37 | -0.00c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

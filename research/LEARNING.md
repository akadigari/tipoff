# What the scanner has learned about itself

_Auto-generated 2026-08-19T14:45:30Z. 10000 candidates logged, 5392 with a filled 24h forward price._

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
| alerted (passed gate and score) | 41 | +0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5172 | -0.10c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 179 | -1.07c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| within_trader | 727 | +0.30c | +0.00c | 56% | NOISE (no measurable edge) |
| price_impact | 212 | +0.16c | -0.52c | 46% | NOISE (no measurable edge) |
| coordination | 9 | +0.08c | +0.50c | 75% | INSUFFICIENT DATA |
| cross_platform | 129 | +0.08c | +0.00c | 48% | NOISE (no measurable edge) |
| thin_market | 51 | +0.03c | +0.05c | 63% | NOISE (no measurable edge) |
| volume_spike | 4752 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1187 | -0.06c | +0.00c | 56% | NOISE (no measurable edge) |
| large_trade | 1661 | -0.08c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 28 | -0.22c | +0.02c | 54% | INSUFFICIENT DATA |
| insiderable | 497 | -0.33c | +0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 745 | -0.98c | -1.00c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 700 | +0.39c | +0.05c | 56% | NOISE (no measurable edge) |
| politics | 2471 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2107 | -0.21c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 107 | -1.90c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 7 | -4.36c | -1.00c | 29% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 768 | -0.07c | +0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3363 | -0.09c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 521 | -0.22c | -0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 740 | -0.34c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4895 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 497 | -0.33c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 67 | +1.09c | -0.00c | 48% | FOLLOW |
| 3 to 7 days | 301 | +0.65c | +0.20c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1204 | -0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| over a month | 3417 | -0.14c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 270 | -1.39c | -0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 66 | +0.09c | 50% |
| p_6h (alerted only) | 58 | +0.35c | 51% |
| p_24h (alerted only) | 41 | +0.08c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

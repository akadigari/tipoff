# What the scanner has learned about itself

_Auto-generated 2026-08-19T11:35:04Z. 10000 candidates logged, 5384 with a filled 24h forward price._

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
| alerted (passed gate and score) | 39 | +0.07c | +0.45c | 54% | NOISE (no measurable edge) |
| filtered out | 5164 | -0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 181 | -1.03c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 55 | +0.56c | +0.05c | 64% | NOISE (no measurable edge) |
| within_trader | 734 | +0.29c | +0.00c | 56% | NOISE (no measurable edge) |
| cross_platform | 131 | +0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| coordination | 8 | +0.02c | +0.40c | 71% | INSUFFICIENT DATA |
| price_impact | 211 | +0.01c | -0.55c | 45% | NOISE (no measurable edge) |
| large_trade | 1681 | -0.05c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1191 | -0.05c | -0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4741 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 29 | -0.11c | +0.05c | 56% | INSUFFICIENT DATA |
| insiderable | 487 | -0.30c | +0.00c | 51% | NOISE (no measurable edge) |
| price_jump | 742 | -1.19c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 666 | +0.31c | +0.00c | 55% | NOISE (no measurable edge) |
| politics | 2473 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2129 | -0.28c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 107 | -1.90c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 9 | -3.94c | -1.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 770 | -0.05c | +0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3347 | -0.13c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 521 | -0.18c | +0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 746 | -0.46c | -0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4897 | -0.16c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 487 | -0.30c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 75 | +1.29c | -0.00c | 48% | FOLLOW |
| 1 to 4 weeks | 1193 | -0.06c | -0.00c | 50% | NOISE (no measurable edge) |
| over a month | 3401 | -0.13c | -0.00c | 47% | NOISE (no measurable edge) |
| 3 to 7 days | 310 | -0.16c | +0.05c | 51% | NOISE (no measurable edge) |
| 1 to 3 days | 272 | -1.33c | +0.00c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 68 | +0.09c | 50% |
| p_6h (alerted only) | 58 | -0.09c | 48% |
| p_24h (alerted only) | 39 | +0.07c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

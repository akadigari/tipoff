# What the scanner has learned about itself

_Auto-generated 2026-08-02T06:41:54Z. 10000 candidates logged, 5753 with a filled 24h forward price._

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
| alerted (passed gate and score) | 63 | +1.30c | +0.50c | 51% | FOLLOW |
| filtered out | 5472 | -0.49c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 218 | -0.74c | +0.00c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 13 | +2.80c | +2.00c | 62% | INSUFFICIENT DATA |
| coordination | 2 | +2.30c | +2.30c | 100% | INSUFFICIENT DATA |
| large_trade | 1996 | -0.27c | +0.00c | 53% | NOISE (no measurable edge) |
| volume_spike | 4733 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| insiderable | 626 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1359 | -0.47c | -0.00c | 53% | NOISE (no measurable edge) |
| within_trader | 828 | -0.73c | +0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 106 | -0.80c | +0.00c | 49% | NOISE (no measurable edge) |
| thin_market | 43 | -1.25c | -0.45c | 37% | FADE (signal points the wrong way) |
| price_jump | 1207 | -1.33c | -1.00c | 47% | FADE (signal points the wrong way) |
| price_impact | 291 | -1.42c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 388 | +0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| sports | 18 | -0.11c | -0.00c | 47% | INSUFFICIENT DATA |
| crypto | 543 | -0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2223 | -0.31c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2581 | -0.82c | -0.00c | 48% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 863 | -0.15c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3436 | -0.40c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 818 | -0.55c | +0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 636 | -1.30c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 626 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| normal | 5127 | -0.50c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 25 | +1.21c | +0.00c | 52% | INSUFFICIENT DATA |
| 3 to 7 days | 549 | +0.19c | +0.15c | 52% | NOISE (no measurable edge) |
| over a month | 3702 | -0.38c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1050 | -0.99c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 337 | -1.28c | -0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 85 | +0.20c | 46% |
| p_6h (alerted only) | 79 | -0.80c | 45% |
| p_24h (alerted only) | 63 | +1.30c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-07-31T23:12:42Z. 10000 candidates logged, 5677 with a filled 24h forward price._

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
| alerted (passed gate and score) | 61 | +0.56c | -1.00c | 47% | NOISE (no measurable edge) |
| filtered out | 5400 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 216 | -1.26c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 14 | +2.60c | +1.32c | 62% | INSUFFICIENT DATA |
| coordination | 2 | +2.30c | +2.30c | 100% | INSUFFICIENT DATA |
| large_trade | 1977 | -0.25c | -0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4650 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1321 | -0.36c | -0.00c | 53% | NOISE (no measurable edge) |
| within_trader | 835 | -0.59c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 647 | -0.64c | +0.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 94 | -0.93c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 292 | -1.28c | -1.00c | 46% | FADE (signal points the wrong way) |
| thin_market | 40 | -1.44c | -0.40c | 37% | FADE (signal points the wrong way) |
| price_jump | 1207 | -1.48c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 17 | +0.32c | -0.00c | 43% | INSUFFICIENT DATA |
| entertainment | 371 | +0.04c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 553 | -0.12c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2160 | -0.30c | -0.00c | 47% | NOISE (no measurable edge) |
| other | 2576 | -0.82c | -0.00c | 47% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 857 | -0.22c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3378 | -0.41c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 819 | -0.60c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 623 | -1.18c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5030 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 647 | -0.64c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 27 | +5.21c | +1.95c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 545 | +0.37c | +0.15c | 52% | NOISE (no measurable edge) |
| over a month | 3539 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1137 | -1.07c | -0.05c | 48% | FADE (signal points the wrong way) |
| 1 to 3 days | 339 | -1.98c | -0.35c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 84 | -0.05c | 44% |
| p_6h (alerted only) | 75 | -0.21c | 48% |
| p_24h (alerted only) | 61 | +0.56c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

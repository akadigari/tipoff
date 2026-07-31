# What the scanner has learned about itself

_Auto-generated 2026-07-31T21:16:59Z. 10000 candidates logged, 5700 with a filled 24h forward price._

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
| alerted (passed gate and score) | 66 | +0.51c | -0.38c | 48% | NOISE (no measurable edge) |
| filtered out | 5417 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 217 | -1.26c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| coordination | 2 | +2.30c | +2.30c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 15 | +1.96c | +0.65c | 57% | INSUFFICIENT DATA |
| large_trade | 1986 | -0.29c | +0.00c | 53% | NOISE (no measurable edge) |
| volume_spike | 4655 | -0.33c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1328 | -0.41c | -0.00c | 53% | NOISE (no measurable edge) |
| insiderable | 653 | -0.59c | -0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 841 | -0.67c | +0.00c | 51% | NOISE (no measurable edge) |
| cross_platform | 95 | -1.06c | +0.00c | 48% | FADE (signal points the wrong way) |
| price_impact | 301 | -1.20c | -1.00c | 46% | FADE (signal points the wrong way) |
| price_jump | 1223 | -1.51c | -1.00c | 46% | FADE (signal points the wrong way) |
| thin_market | 40 | -1.54c | -0.47c | 34% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 18 | +0.56c | -0.00c | 47% | INSUFFICIENT DATA |
| entertainment | 368 | -0.05c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 552 | -0.12c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2163 | -0.27c | -0.00c | 47% | NOISE (no measurable edge) |
| other | 2599 | -0.85c | -0.00c | 47% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 860 | -0.20c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3388 | -0.42c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 825 | -0.60c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 627 | -1.26c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5047 | -0.49c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 653 | -0.59c | -0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 26 | +5.41c | +2.92c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 540 | +0.25c | +0.10c | 51% | NOISE (no measurable edge) |
| over a month | 3551 | -0.32c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1152 | -1.06c | -0.02c | 48% | FADE (signal points the wrong way) |
| 1 to 3 days | 342 | -2.02c | -0.33c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 89 | -0.14c | 44% |
| p_6h (alerted only) | 79 | +0.14c | 51% |
| p_24h (alerted only) | 66 | +0.51c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

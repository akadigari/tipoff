# What the scanner has learned about itself

_Auto-generated 2026-08-20T14:47:47Z. 10000 candidates logged, 5185 with a filled 24h forward price._

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
| alerted (passed gate and score) | 35 | +0.51c | +0.45c | 53% | NOISE (no measurable edge) |
| filtered out | 4983 | -0.19c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 167 | -0.64c | -0.00c | 54% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 8 | +0.84c | +0.55c | 86% | INSUFFICIENT DATA |
| cross_platform | 123 | +0.83c | -0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 699 | +0.35c | +0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4562 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1534 | -0.16c | -0.00c | 55% | NOISE (no measurable edge) |
| thin_market | 46 | -0.19c | +0.08c | 64% | NOISE (no measurable edge) |
| repeat_actor | 1103 | -0.29c | +0.05c | 57% | NOISE (no measurable edge) |
| fresh_wallet | 24 | -0.43c | +0.05c | 57% | INSUFFICIENT DATA |
| insiderable | 464 | -0.43c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 209 | -0.48c | -0.65c | 45% | NOISE (no measurable edge) |
| price_jump | 692 | -1.68c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 671 | +0.03c | +0.05c | 55% | NOISE (no measurable edge) |
| politics | 2452 | -0.02c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 1951 | -0.42c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 111 | -1.83c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 477 | -0.14c | -0.00c | 55% | NOISE (no measurable edge) |
| under 40 | 3311 | -0.15c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 671 | -0.27c | -0.00c | 49% | NOISE (no measurable edge) |
| 55 to 69 | 726 | -0.42c | +0.00c | 55% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4721 | -0.18c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 464 | -0.43c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 55 | +4.49c | +0.00c | 51% | FOLLOW |
| over a month | 3390 | -0.18c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1116 | -0.42c | -0.00c | 49% | NOISE (no measurable edge) |
| 3 to 7 days | 239 | -0.49c | +0.25c | 54% | NOISE (no measurable edge) |
| 1 to 3 days | 252 | -1.29c | +0.05c | 52% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 83 | +1.82c | 56% |
| p_6h (alerted only) | 66 | +3.06c | 55% |
| p_24h (alerted only) | 35 | +0.51c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

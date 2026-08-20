# What the scanner has learned about itself

_Auto-generated 2026-08-20T22:38:01Z. 10000 candidates logged, 5366 with a filled 24h forward price._

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
| alerted (passed gate and score) | 44 | +2.76c | +0.22c | 51% | FOLLOW |
| filtered out | 5151 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 171 | -0.56c | +0.00c | 54% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 8 | +0.84c | +0.55c | 86% | INSUFFICIENT DATA |
| cross_platform | 121 | +0.72c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 214 | +0.66c | -0.05c | 48% | NOISE (no measurable edge) |
| within_trader | 717 | +0.29c | -0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4719 | +0.04c | -0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1586 | -0.17c | +0.00c | 55% | NOISE (no measurable edge) |
| thin_market | 44 | -0.19c | +0.10c | 66% | NOISE (no measurable edge) |
| repeat_actor | 1144 | -0.27c | +0.05c | 56% | NOISE (no measurable edge) |
| insiderable | 469 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.45c | +0.05c | 57% | INSUFFICIENT DATA |
| price_jump | 733 | -1.29c | -1.00c | 47% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 816 | +0.47c | +0.15c | 57% | NOISE (no measurable edge) |
| politics | 2410 | +0.02c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2027 | -0.37c | -0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 113 | -1.85c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 486 | +0.28c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3419 | -0.05c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 694 | -0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| 55 to 69 | 767 | -0.49c | +0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4897 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 469 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 53 | +4.49c | +0.00c | 49% | FOLLOW |
| over a month | 3449 | -0.07c | +0.00c | 47% | NOISE (no measurable edge) |
| 3 to 7 days | 244 | -0.27c | +0.25c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1198 | -0.43c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 287 | -0.46c | +0.15c | 54% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 79 | +2.55c | 56% |
| p_6h (alerted only) | 69 | +3.06c | 57% |
| p_24h (alerted only) | 44 | +2.76c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

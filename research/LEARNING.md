# What the scanner has learned about itself

_Auto-generated 2026-08-20T21:37:24Z. 10000 candidates logged, 5338 with a filled 24h forward price._

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
| alerted (passed gate and score) | 41 | +2.51c | +0.45c | 52% | FOLLOW |
| filtered out | 5126 | -0.12c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 171 | -0.56c | +0.00c | 54% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 8 | +0.84c | +0.55c | 86% | INSUFFICIENT DATA |
| cross_platform | 122 | +0.72c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 213 | +0.52c | -0.10c | 48% | NOISE (no measurable edge) |
| within_trader | 710 | +0.21c | +0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4694 | +0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| thin_market | 44 | -0.19c | +0.10c | 66% | NOISE (no measurable edge) |
| large_trade | 1578 | -0.22c | +0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 472 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |
| repeat_actor | 1139 | -0.37c | -0.00c | 56% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.45c | +0.05c | 57% | INSUFFICIENT DATA |
| price_jump | 727 | -1.39c | -1.00c | 47% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 800 | +0.37c | +0.10c | 57% | NOISE (no measurable edge) |
| politics | 2405 | +0.02c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2020 | -0.38c | -0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 113 | -1.85c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 483 | +0.20c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3398 | -0.07c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 694 | -0.11c | -0.00c | 49% | NOISE (no measurable edge) |
| 55 to 69 | 763 | -0.52c | +0.00c | 55% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4866 | -0.10c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 472 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 54 | +4.44c | +0.00c | 50% | FOLLOW |
| over a month | 3428 | -0.07c | +0.00c | 47% | NOISE (no measurable edge) |
| 3 to 7 days | 245 | -0.30c | +0.25c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1193 | -0.46c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 284 | -0.68c | +0.10c | 54% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 81 | +2.52c | 57% |
| p_6h (alerted only) | 69 | +3.12c | 57% |
| p_24h (alerted only) | 41 | +2.51c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

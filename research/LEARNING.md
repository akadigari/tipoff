# What the scanner has learned about itself

_Auto-generated 2026-08-20T13:53:37Z. 10000 candidates logged, 5177 with a filled 24h forward price._

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
| filtered out | 4977 | -0.18c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 166 | -0.77c | -0.00c | 54% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 34 | -1.43c | +0.22c | 52% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 8 | +0.84c | +0.55c | 86% | INSUFFICIENT DATA |
| cross_platform | 118 | +0.58c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 698 | +0.35c | +0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4546 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1534 | -0.08c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1103 | -0.17c | +0.05c | 57% | NOISE (no measurable edge) |
| thin_market | 46 | -0.19c | +0.08c | 64% | NOISE (no measurable edge) |
| insiderable | 466 | -0.40c | +0.00c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.45c | +0.05c | 55% | INSUFFICIENT DATA |
| price_impact | 213 | -0.53c | -0.55c | 45% | NOISE (no measurable edge) |
| price_jump | 693 | -1.79c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 670 | +0.10c | +0.05c | 55% | NOISE (no measurable edge) |
| politics | 2447 | -0.02c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 1948 | -0.46c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 112 | -1.77c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3310 | -0.17c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 724 | -0.26c | +0.00c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 672 | -0.27c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 471 | -0.30c | -0.00c | 55% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4711 | -0.19c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 466 | -0.40c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 55 | +4.49c | +0.00c | 51% | FOLLOW |
| over a month | 3384 | -0.21c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1111 | -0.29c | +0.00c | 50% | NOISE (no measurable edge) |
| 3 to 7 days | 244 | -0.44c | +0.33c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 250 | -1.76c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 83 | +1.82c | 56% |
| p_6h (alerted only) | 66 | +3.06c | 55% |
| p_24h (alerted only) | 34 | -1.43c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

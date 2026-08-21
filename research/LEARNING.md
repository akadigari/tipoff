# What the scanner has learned about itself

_Auto-generated 2026-08-21T18:50:43Z. 10000 candidates logged, 5390 with a filled 24h forward price._

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
| alerted (passed gate and score) | 44 | +3.41c | +0.47c | 53% | FOLLOW |
| filtered out | 5176 | -0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 170 | -0.84c | -0.00c | 53% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 218 | +1.01c | +0.50c | 52% | FOLLOW |
| cross_platform | 108 | +0.93c | +0.00c | 48% | NOISE (no measurable edge) |
| volume_spike | 4763 | +0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 735 | +0.04c | +0.00c | 57% | NOISE (no measurable edge) |
| coordination | 9 | -0.24c | +0.60c | 88% | INSUFFICIENT DATA |
| insiderable | 448 | -0.27c | +0.00c | 46% | NOISE (no measurable edge) |
| price_jump | 733 | -0.30c | +0.00c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 22 | -0.47c | +0.05c | 58% | INSUFFICIENT DATA |
| large_trade | 1622 | -0.49c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 40 | -0.57c | +0.08c | 63% | NOISE (no measurable edge) |
| repeat_actor | 1164 | -0.62c | +0.05c | 56% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 940 | +0.90c | +0.23c | 57% | NOISE (no measurable edge) |
| politics | 2260 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2099 | -0.36c | -0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 91 | -2.11c | -0.50c | 43% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3423 | +0.13c | -0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 684 | +0.10c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 514 | -0.00c | +0.00c | 57% | NOISE (no measurable edge) |
| 55 to 69 | 769 | -0.66c | -0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4942 | +0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 448 | -0.27c | +0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 49 | +4.69c | +0.00c | 49% | FOLLOW |
| 3 to 7 days | 245 | +0.82c | +0.25c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 289 | +0.46c | +0.35c | 55% | NOISE (no measurable edge) |
| over a month | 3375 | -0.05c | -0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1286 | -0.44c | +0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 83 | +1.88c | 56% |
| p_6h (alerted only) | 71 | +2.72c | 52% |
| p_24h (alerted only) | 44 | +3.41c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

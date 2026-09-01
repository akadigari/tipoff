# What the scanner has learned about itself

_Auto-generated 2026-09-01T23:14:35Z. 10000 candidates logged, 6552 with a filled 24h forward price._

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
| alerted (passed gate and score) | 72 | +1.77c | +0.00c | 51% | FOLLOW |
| filtered out | 6226 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 254 | -1.03c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 340 | +0.62c | -0.50c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 24 | +0.39c | +0.00c | 45% | INSUFFICIENT DATA |
| cross_platform | 73 | +0.17c | +0.00c | 42% | NOISE (no measurable edge) |
| insiderable | 597 | +0.08c | -0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 5770 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 974 | -0.37c | +0.00c | 54% | NOISE (no measurable edge) |
| large_trade | 2277 | -0.45c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1648 | -0.56c | +0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 920 | -0.60c | -0.62c | 48% | NOISE (no measurable edge) |
| coordination | 11 | -0.74c | -0.00c | 56% | INSUFFICIENT DATA |
| thin_market | 44 | -2.60c | +0.08c | 57% | FADE (signal points the wrong way) |
| chatter | 6 | -3.58c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2294 | +0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 1556 | -0.03c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2588 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 114 | -1.40c | -0.50c | 41% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3859 | +0.22c | +0.00c | 48% | NOISE (no measurable edge) |
| 40 to 54 | 873 | -0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 1045 | -0.50c | +0.00c | 52% | NOISE (no measurable edge) |
| 70+ | 775 | -0.73c | -0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 597 | +0.08c | -0.00c | 50% | NOISE (no measurable edge) |
| normal | 5955 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 559 | +0.80c | +0.30c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 323 | +0.10c | +0.20c | 51% | NOISE (no measurable edge) |
| over a month | 4115 | +0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1453 | -0.64c | -0.00c | 48% | NOISE (no measurable edge) |
| under 1 day | 15 | -4.04c | -7.50c | 47% | INSUFFICIENT DATA |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 104 | +1.08c | 55% |
| p_6h (alerted only) | 93 | +2.94c | 55% |
| p_24h (alerted only) | 72 | +1.77c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

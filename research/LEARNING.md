# What the scanner has learned about itself

_Auto-generated 2026-08-29T04:07:08Z. 10000 candidates logged, 6529 with a filled 24h forward price._

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
| alerted (passed gate and score) | 65 | +1.25c | +0.00c | 48% | FOLLOW |
| filtered out | 6232 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 232 | -1.08c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 65 | +1.20c | +0.00c | 47% | FOLLOW |
| insiderable | 580 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 347 | +0.05c | -0.85c | 47% | NOISE (no measurable edge) |
| volume_spike | 5739 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 942 | -0.19c | +0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 21 | -0.23c | +0.00c | 41% | INSUFFICIENT DATA |
| large_trade | 2184 | -0.38c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1601 | -0.53c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 926 | -1.00c | -0.75c | 48% | FADE (signal points the wrong way) |
| coordination | 7 | -1.34c | -0.20c | 43% | INSUFFICIENT DATA |
| thin_market | 34 | -2.81c | +0.08c | 56% | FADE (signal points the wrong way) |
| chatter | 6 | -3.58c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2309 | +0.01c | -0.00c | 50% | NOISE (no measurable edge) |
| crypto | 1560 | -0.12c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2552 | -0.15c | -0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 108 | -1.44c | -1.00c | 37% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 841 | +0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3921 | +0.08c | -0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 1029 | -0.54c | -0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 738 | -0.79c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 580 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| normal | 5949 | -0.13c | -0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 557 | +0.55c | +0.30c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 282 | +0.17c | +0.85c | 53% | NOISE (no measurable edge) |
| over a month | 4066 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1504 | -0.74c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 96 | +1.24c | 55% |
| p_6h (alerted only) | 85 | +2.97c | 53% |
| p_24h (alerted only) | 65 | +1.25c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

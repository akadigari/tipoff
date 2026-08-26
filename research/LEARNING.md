# What the scanner has learned about itself

_Auto-generated 2026-08-26T08:56:34Z. 10000 candidates logged, 5764 with a filled 24h forward price._

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
| alerted (passed gate and score) | 61 | +0.24c | -0.50c | 46% | NOISE (no measurable edge) |
| filtered out | 5492 | -0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 211 | -1.08c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 60 | +1.25c | +0.00c | 43% | FOLLOW |
| price_impact | 313 | +0.33c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 511 | +0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| volume_spike | 5047 | -0.04c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 845 | -0.18c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1935 | -0.45c | -0.00c | 51% | NOISE (no measurable edge) |
| fresh_wallet | 15 | -0.49c | -0.05c | 25% | INSUFFICIENT DATA |
| price_jump | 830 | -0.53c | -0.05c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1426 | -0.58c | +0.00c | 53% | NOISE (no measurable edge) |
| coordination | 7 | -1.13c | +0.25c | 57% | INSUFFICIENT DATA |
| thin_market | 34 | -2.99c | +0.00c | 50% | FADE (signal points the wrong way) |
| chatter | 1 | -3.50c | -3.50c | 0% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1445 | +0.07c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 1983 | -0.01c | -0.00c | 48% | NOISE (no measurable edge) |
| other | 2241 | -0.16c | +0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 95 | -1.06c | -1.00c | 35% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 749 | +0.29c | -0.00c | 50% | NOISE (no measurable edge) |
| under 40 | 3456 | +0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 908 | -0.54c | +0.00c | 52% | NOISE (no measurable edge) |
| 70+ | 651 | -0.66c | -0.00c | 49% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 511 | +0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| normal | 5253 | -0.08c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 301 | +1.70c | +0.25c | 53% | FOLLOW |
| over a month | 3551 | -0.03c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 256 | -0.24c | +0.98c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1531 | -0.70c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.01c | 54% |
| p_6h (alerted only) | 82 | +2.83c | 55% |
| p_24h (alerted only) | 61 | +0.24c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

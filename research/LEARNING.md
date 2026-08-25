# What the scanner has learned about itself

_Auto-generated 2026-08-25T19:39:56Z. 10000 candidates logged, 5670 with a filled 24h forward price._

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
| filtered out | 5403 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 57 | -0.24c | -0.50c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 210 | -0.96c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 72 | +1.10c | +0.00c | 45% | FOLLOW |
| price_impact | 299 | +0.47c | -0.50c | 48% | NOISE (no measurable edge) |
| volume_spike | 4993 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 516 | -0.04c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 833 | -0.05c | -0.00c | 55% | NOISE (no measurable edge) |
| fresh_wallet | 14 | -0.40c | -0.05c | 33% | INSUFFICIENT DATA |
| large_trade | 1868 | -0.42c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 786 | -0.49c | +0.00c | 50% | NOISE (no measurable edge) |
| repeat_actor | 1383 | -0.52c | +0.00c | 54% | NOISE (no measurable edge) |
| coordination | 9 | -0.78c | +0.25c | 62% | INSUFFICIENT DATA |
| thin_market | 33 | -2.89c | -0.00c | 50% | FADE (signal points the wrong way) |
| chatter | 1 | -3.50c | -3.50c | 0% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1368 | +0.17c | +0.05c | 52% | NOISE (no measurable edge) |
| politics | 2008 | +0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2199 | -0.23c | -0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 95 | -0.89c | -0.50c | 39% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 740 | +0.28c | +0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3410 | +0.07c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 879 | -0.50c | +0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 641 | -0.54c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 516 | -0.04c | +0.00c | 48% | NOISE (no measurable edge) |
| normal | 5154 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 27 | +6.42c | -0.00c | 52% | INSUFFICIENT DATA |
| 3 to 7 days | 233 | +1.12c | +0.15c | 52% | FOLLOW |
| over a month | 3526 | +0.02c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 248 | -0.09c | +0.85c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1523 | -0.64c | +0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.04c | 55% |
| p_6h (alerted only) | 83 | +2.78c | 54% |
| p_24h (alerted only) | 57 | -0.24c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

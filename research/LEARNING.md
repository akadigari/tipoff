# What the scanner has learned about itself

_Auto-generated 2026-08-25T08:54:15Z. 10000 candidates logged, 5613 with a filled 24h forward price._

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
| filtered out | 5351 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 207 | -0.81c | +0.00c | 52% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 55 | -0.99c | -0.50c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 78 | +1.07c | +0.00c | 45% | FOLLOW |
| price_impact | 292 | +0.82c | -0.50c | 48% | NOISE (no measurable edge) |
| within_trader | 833 | +0.06c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4950 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 522 | -0.06c | +0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 766 | -0.21c | -0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 15 | -0.27c | -0.05c | 38% | INSUFFICIENT DATA |
| large_trade | 1832 | -0.47c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1362 | -0.54c | +0.00c | 54% | NOISE (no measurable edge) |
| coordination | 7 | -0.63c | +0.60c | 83% | INSUFFICIENT DATA |
| thin_market | 34 | -2.76c | +0.03c | 52% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1320 | +0.42c | +0.10c | 54% | NOISE (no measurable edge) |
| politics | 2022 | +0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2178 | -0.35c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 93 | -0.84c | -0.00c | 42% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 729 | +0.23c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3392 | +0.10c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 638 | -0.30c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 854 | -0.60c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5091 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 522 | -0.06c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 37 | +4.93c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 223 | +1.49c | +0.25c | 53% | FOLLOW |
| over a month | 3483 | +0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 249 | -0.00c | +0.50c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1505 | -0.57c | -0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 96 | +0.97c | 54% |
| p_6h (alerted only) | 81 | +2.35c | 51% |
| p_24h (alerted only) | 55 | -0.99c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

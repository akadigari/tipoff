# What the scanner has learned about itself

_Auto-generated 2026-08-18T22:35:06Z. 10000 candidates logged, 5556 with a filled 24h forward price._

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
| filtered out | 5328 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 42 | -0.77c | +0.22c | 52% | NOISE (no measurable edge) |
| monitor (strong but gated) | 186 | -0.78c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 59 | +0.90c | +0.50c | 71% | NOISE (no measurable edge) |
| within_trader | 764 | +0.59c | +0.05c | 59% | NOISE (no measurable edge) |
| large_trade | 1769 | +0.21c | +0.00c | 56% | NOISE (no measurable edge) |
| repeat_actor | 1251 | +0.20c | +0.10c | 57% | NOISE (no measurable edge) |
| coordination | 10 | +0.11c | +0.40c | 75% | INSUFFICIENT DATA |
| volume_spike | 4899 | +0.06c | -0.00c | 50% | NOISE (no measurable edge) |
| cross_platform | 134 | +0.05c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 214 | +0.04c | -0.50c | 46% | NOISE (no measurable edge) |
| fresh_wallet | 33 | -0.20c | -0.00c | 52% | NOISE (no measurable edge) |
| insiderable | 507 | -0.23c | -0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 761 | -1.22c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 668 | +0.43c | +0.05c | 55% | NOISE (no measurable edge) |
| politics | 2556 | -0.04c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2214 | -0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 107 | -1.34c | -0.00c | 49% | FADE (signal points the wrong way) |
| sports | 11 | -4.82c | -6.00c | 27% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 809 | +0.18c | +0.00c | 56% | NOISE (no measurable edge) |
| 70+ | 551 | +0.08c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3438 | -0.11c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 758 | -0.31c | -0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5049 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 507 | -0.23c | -0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 78 | +1.97c | +0.00c | 50% | FOLLOW |
| 3 to 7 days | 351 | +0.69c | +0.25c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1226 | +0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3464 | -0.14c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 297 | -1.16c | -0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 70 | -0.25c | 44% |
| p_6h (alerted only) | 62 | -0.37c | 46% |
| p_24h (alerted only) | 42 | -0.77c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

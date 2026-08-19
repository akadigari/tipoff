# What the scanner has learned about itself

_Auto-generated 2026-08-19T17:35:18Z. 10000 candidates logged, 5290 with a filled 24h forward price._

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
| alerted (passed gate and score) | 41 | +0.08c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5074 | -0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 175 | -1.26c | -0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 123 | +0.50c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 717 | +0.27c | -0.00c | 55% | NOISE (no measurable edge) |
| price_impact | 211 | +0.24c | -0.55c | 45% | NOISE (no measurable edge) |
| coordination | 9 | +0.08c | +0.50c | 75% | INSUFFICIENT DATA |
| thin_market | 50 | +0.00c | +0.05c | 60% | NOISE (no measurable edge) |
| volume_spike | 4662 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1159 | -0.12c | -0.00c | 55% | NOISE (no measurable edge) |
| large_trade | 1621 | -0.16c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 27 | -0.22c | +0.05c | 57% | INSUFFICIENT DATA |
| insiderable | 487 | -0.27c | +0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 721 | -1.36c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 703 | +0.36c | +0.05c | 55% | NOISE (no measurable edge) |
| politics | 2419 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2057 | -0.36c | -0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 106 | -1.91c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 5 | -5.80c | -6.00c | 40% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3317 | -0.12c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 752 | -0.23c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 504 | -0.29c | +0.00c | 53% | NOISE (no measurable edge) |
| 40 to 54 | 717 | -0.29c | -0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4803 | -0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 487 | -0.27c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 62 | +1.84c | +0.00c | 50% | FOLLOW |
| 3 to 7 days | 291 | +0.17c | +0.20c | 53% | NOISE (no measurable edge) |
| over a month | 3368 | -0.13c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1170 | -0.23c | -0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 267 | -1.13c | -0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 71 | +1.07c | 52% |
| p_6h (alerted only) | 58 | +0.07c | 51% |
| p_24h (alerted only) | 41 | +0.08c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

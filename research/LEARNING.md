# What the scanner has learned about itself

_Auto-generated 2026-08-17T05:43:42Z. 10000 candidates logged, 5758 with a filled 24h forward price._

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
| filtered out | 5484 | +0.13c | -0.00c | 50% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 62 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 212 | -0.81c | +0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 138 | +1.22c | +0.00c | 52% | FOLLOW |
| thin_market | 83 | +1.00c | +0.30c | 68% | FOLLOW |
| within_trader | 798 | +0.92c | +0.10c | 59% | NOISE (no measurable edge) |
| repeat_actor | 1302 | +0.71c | +0.10c | 60% | NOISE (no measurable edge) |
| large_trade | 1846 | +0.63c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 5004 | +0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 249 | +0.07c | -0.45c | 48% | NOISE (no measurable edge) |
| insiderable | 534 | +0.01c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 29 | -0.42c | -0.05c | 42% | INSUFFICIENT DATA |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_jump | 881 | -0.55c | +0.00c | 48% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 617 | +0.28c | +0.00c | 53% | NOISE (no measurable edge) |
| politics | 2586 | +0.16c | -0.00c | 51% | NOISE (no measurable edge) |
| other | 2405 | +0.08c | -0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 135 | -1.20c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 15 | -3.40c | -1.00c | 36% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 833 | +0.54c | +0.05c | 57% | NOISE (no measurable edge) |
| 70+ | 582 | +0.32c | -0.00c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 786 | +0.19c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3557 | -0.06c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5224 | +0.11c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 534 | +0.01c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 75 | +1.22c | +0.25c | 53% | FOLLOW |
| 3 to 7 days | 421 | +0.75c | +0.20c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1265 | +0.45c | +0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 361 | +0.14c | +0.05c | 53% | NOISE (no measurable edge) |
| over a month | 3500 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 89 | +0.33c | 52% |
| p_6h (alerted only) | 84 | +0.45c | 48% |
| p_24h (alerted only) | 62 | +0.12c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-15T03:00:13Z. 10000 candidates logged, 5607 with a filled 24h forward price._

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
| alerted (passed gate and score) | 72 | +0.82c | +1.00c | 52% | NOISE (no measurable edge) |
| filtered out | 5324 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 211 | -1.12c | -0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 69 | +1.65c | +0.50c | 68% | FOLLOW |
| cross_platform | 163 | +1.35c | +0.00c | 51% | FOLLOW |
| repeat_actor | 1287 | +0.87c | +0.15c | 59% | NOISE (no measurable edge) |
| within_trader | 753 | +0.86c | +0.10c | 60% | NOISE (no measurable edge) |
| large_trade | 1844 | +0.77c | +0.10c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 25 | +0.53c | +0.00c | 48% | INSUFFICIENT DATA |
| volume_spike | 4827 | +0.26c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 489 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 895 | -0.19c | -0.00c | 50% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 259 | -0.78c | -0.55c | 45% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 564 | +0.33c | -0.00c | 53% | NOISE (no measurable edge) |
| politics | 2467 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2429 | +0.16c | -0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 127 | -0.24c | -0.00c | 43% | NOISE (no measurable edge) |
| sports | 20 | -4.63c | -3.25c | 32% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 819 | +0.78c | +0.10c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 804 | +0.39c | +0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 566 | +0.28c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3418 | -0.06c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5118 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| high | 489 | +0.10c | +0.00c | 54% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 65 | +1.51c | +0.30c | 54% | FOLLOW |
| 3 to 7 days | 416 | +1.49c | +0.30c | 57% | FOLLOW |
| 1 to 4 weeks | 1278 | +0.49c | +0.05c | 54% | NOISE (no measurable edge) |
| 1 to 3 days | 327 | +0.28c | +0.30c | 55% | NOISE (no measurable edge) |
| over a month | 3420 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 100 | -0.20c | 45% |
| p_6h (alerted only) | 95 | -0.25c | 45% |
| p_24h (alerted only) | 72 | +0.82c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

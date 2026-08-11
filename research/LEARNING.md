# What the scanner has learned about itself

_Auto-generated 2026-08-11T17:10:33Z. 10000 candidates logged, 5701 with a filled 24h forward price._

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
| alerted (passed gate and score) | 84 | +1.11c | +0.58c | 52% | FOLLOW |
| filtered out | 5372 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 245 | -0.45c | -0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 166 | +1.06c | +0.00c | 51% | FOLLOW |
| thin_market | 69 | +0.83c | +0.30c | 62% | NOISE (no measurable edge) |
| fresh_wallet | 21 | +0.82c | -0.10c | 45% | INSUFFICIENT DATA |
| repeat_actor | 1379 | +0.40c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1978 | +0.35c | +0.05c | 57% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4874 | +0.00c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 835 | -0.05c | +0.05c | 58% | NOISE (no measurable edge) |
| price_jump | 943 | -0.06c | -0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 496 | -0.40c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 260 | -1.15c | -0.50c | 47% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2319 | +0.06c | -0.00c | 50% | NOISE (no measurable edge) |
| crypto | 498 | +0.04c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2664 | -0.14c | -0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 194 | -0.58c | -0.10c | 43% | NOISE (no measurable edge) |
| sports | 26 | -4.67c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 836 | +0.41c | +0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 805 | +0.26c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3439 | -0.25c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 621 | -0.26c | +0.00c | 58% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5205 | -0.05c | -0.00c | 50% | NOISE (no measurable edge) |
| high | 496 | -0.40c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 370 | +1.63c | +0.42c | 58% | FOLLOW |
| 1 to 4 weeks | 1187 | +0.56c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3583 | -0.31c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 415 | -1.05c | +0.05c | 51% | FADE (signal points the wrong way) |
| under 1 day | 63 | -4.40c | +0.00c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 114 | +0.50c | 47% |
| p_6h (alerted only) | 110 | -0.77c | 43% |
| p_24h (alerted only) | 84 | +1.11c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

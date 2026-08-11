# What the scanner has learned about itself

_Auto-generated 2026-08-11T23:52:39Z. 10000 candidates logged, 5705 with a filled 24h forward price._

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
| alerted (passed gate and score) | 82 | +0.81c | +0.08c | 51% | NOISE (no measurable edge) |
| filtered out | 5379 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 244 | -0.65c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 72 | +0.94c | +0.37c | 62% | NOISE (no measurable edge) |
| fresh_wallet | 22 | +0.92c | -0.05c | 48% | INSUFFICIENT DATA |
| cross_platform | 171 | +0.90c | +0.00c | 50% | NOISE (no measurable edge) |
| repeat_actor | 1376 | +0.45c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1965 | +0.41c | +0.05c | 57% | NOISE (no measurable edge) |
| price_jump | 897 | +0.25c | -0.00c | 50% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| within_trader | 840 | +0.09c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4902 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| insiderable | 502 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 261 | -0.91c | -0.50c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2342 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2643 | +0.09c | -0.00c | 51% | NOISE (no measurable edge) |
| crypto | 504 | +0.04c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 189 | -0.55c | -0.05c | 43% | NOISE (no measurable edge) |
| sports | 27 | -5.02c | -4.50c | 23% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 835 | +0.55c | -0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 802 | +0.39c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3456 | -0.06c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 612 | -0.45c | +0.00c | 57% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5203 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 502 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 370 | +1.68c | +0.37c | 57% | FOLLOW |
| 1 to 4 weeks | 1222 | +0.53c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3571 | -0.18c | -0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 386 | -0.54c | +0.05c | 52% | NOISE (no measurable edge) |
| under 1 day | 72 | -3.44c | +0.03c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 114 | +0.54c | 47% |
| p_6h (alerted only) | 110 | -1.24c | 41% |
| p_24h (alerted only) | 82 | +0.81c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

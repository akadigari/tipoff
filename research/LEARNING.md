# What the scanner has learned about itself

_Auto-generated 2026-08-04T10:47:48Z. 10000 candidates logged, 5916 with a filled 24h forward price._

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
| alerted (passed gate and score) | 69 | -0.12c | -1.00c | 46% | NOISE (no measurable edge) |
| filtered out | 5608 | -0.33c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 239 | -0.54c | +0.00c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 18 | +2.57c | +0.40c | 59% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 11 | +0.15c | +2.00c | 70% | INSUFFICIENT DATA |
| volume_spike | 4879 | -0.24c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2078 | -0.29c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1439 | -0.31c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 631 | -0.62c | -0.00c | 48% | NOISE (no measurable edge) |
| cross_platform | 115 | -0.68c | -0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 879 | -0.70c | -0.00c | 53% | NOISE (no measurable edge) |
| price_impact | 285 | -0.72c | -0.50c | 47% | NOISE (no measurable edge) |
| price_jump | 1214 | -0.88c | -1.00c | 47% | NOISE (no measurable edge) |
| thin_market | 44 | -1.97c | -0.30c | 38% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 538 | +0.27c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 378 | -0.20c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2329 | -0.22c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2647 | -0.57c | -0.00c | 47% | NOISE (no measurable edge) |
| sports | 24 | -1.52c | -1.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3534 | -0.21c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 883 | -0.24c | +0.00c | 53% | NOISE (no measurable edge) |
| 40 to 54 | 833 | -0.49c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 666 | -0.90c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5285 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 631 | -0.62c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 557 | +0.46c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3852 | -0.30c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 983 | -0.41c | -0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 393 | -1.54c | -0.25c | 48% | FADE (signal points the wrong way) |
| under 1 day | 32 | -3.26c | +0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 96 | +0.49c | 42% |
| p_6h (alerted only) | 90 | -0.94c | 44% |
| p_24h (alerted only) | 69 | -0.12c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-11T21:58:10Z. 10000 candidates logged, 5712 with a filled 24h forward price._

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
| alerted (passed gate and score) | 82 | +1.06c | +0.08c | 51% | FOLLOW |
| filtered out | 5387 | +0.04c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 243 | -0.54c | -0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 167 | +1.00c | +0.00c | 50% | FOLLOW |
| fresh_wallet | 22 | +0.92c | -0.05c | 48% | INSUFFICIENT DATA |
| thin_market | 71 | +0.87c | +0.30c | 61% | NOISE (no measurable edge) |
| repeat_actor | 1380 | +0.44c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1974 | +0.40c | +0.05c | 57% | NOISE (no measurable edge) |
| price_jump | 904 | +0.20c | -0.00c | 50% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| within_trader | 841 | +0.09c | +0.05c | 58% | NOISE (no measurable edge) |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4906 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 494 | -0.44c | +0.00c | 46% | NOISE (no measurable edge) |
| price_impact | 262 | -0.95c | -0.50c | 46% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2327 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 507 | +0.11c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2659 | +0.03c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 192 | -0.58c | -0.10c | 43% | NOISE (no measurable edge) |
| sports | 27 | -5.02c | -4.50c | 23% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 833 | +0.54c | +0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 806 | +0.34c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3457 | -0.09c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 616 | -0.43c | +0.00c | 57% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5218 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 494 | -0.44c | +0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 368 | +1.75c | +0.40c | 57% | FOLLOW |
| 1 to 4 weeks | 1215 | +0.53c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3586 | -0.21c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 393 | -0.52c | +0.10c | 52% | NOISE (no measurable edge) |
| under 1 day | 67 | -3.82c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 115 | +0.44c | 46% |
| p_6h (alerted only) | 110 | -1.18c | 41% |
| p_24h (alerted only) | 82 | +1.06c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

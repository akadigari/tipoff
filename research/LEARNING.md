# What the scanner has learned about itself

_Auto-generated 2026-08-18T13:50:54Z. 10000 candidates logged, 5648 with a filled 24h forward price._

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
| filtered out | 5404 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 47 | -0.19c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 197 | -0.58c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 133 | +0.89c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 784 | +0.74c | +0.05c | 59% | NOISE (no measurable edge) |
| thin_market | 78 | +0.66c | +0.10c | 66% | NOISE (no measurable edge) |
| price_impact | 229 | +0.66c | -0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1818 | +0.34c | +0.00c | 56% | NOISE (no measurable edge) |
| repeat_actor | 1278 | +0.34c | +0.05c | 57% | NOISE (no measurable edge) |
| volume_spike | 4955 | +0.12c | -0.00c | 50% | NOISE (no measurable edge) |
| coordination | 8 | +0.04c | +0.40c | 71% | INSUFFICIENT DATA |
| insiderable | 508 | -0.16c | +0.00c | 52% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.22c | -0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 807 | -0.90c | -0.50c | 47% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 653 | +0.36c | +0.00c | 55% | NOISE (no measurable edge) |
| politics | 2580 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2280 | -0.10c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 121 | -0.72c | -0.00c | 50% | NOISE (no measurable edge) |
| sports | 14 | -3.50c | -0.75c | 38% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 828 | +0.31c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 565 | +0.23c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3495 | -0.04c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 760 | -0.13c | +0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5140 | +0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 508 | -0.16c | +0.00c | 52% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 76 | +1.56c | +0.33c | 56% | FOLLOW |
| 3 to 7 days | 373 | +0.82c | +0.20c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1255 | +0.29c | -0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3469 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 334 | -0.65c | +0.05c | 53% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 69 | -0.09c | 47% |
| p_6h (alerted only) | 65 | -0.42c | 44% |
| p_24h (alerted only) | 47 | -0.19c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

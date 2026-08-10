# What the scanner has learned about itself

_Auto-generated 2026-08-10T16:06:31Z. 10000 candidates logged, 5776 with a filled 24h forward price._

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
| alerted (passed gate and score) | 85 | +1.78c | +1.00c | 54% | FOLLOW |
| filtered out | 5448 | -0.18c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 243 | -0.50c | +0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 167 | +1.54c | +0.00c | 55% | FOLLOW |
| fresh_wallet | 18 | +0.74c | -0.05c | 47% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| thin_market | 67 | +0.13c | -0.00c | 57% | NOISE (no measurable edge) |
| repeat_actor | 1352 | +0.13c | +0.10c | 56% | NOISE (no measurable edge) |
| large_trade | 1953 | +0.05c | +0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4870 | -0.09c | -0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 1025 | -0.19c | +0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 501 | -0.22c | +0.00c | 45% | NOISE (no measurable edge) |
| within_trader | 839 | -0.35c | +0.00c | 56% | NOISE (no measurable edge) |
| coordination | 2 | -0.37c | -0.37c | 50% | INSUFFICIENT DATA |
| price_impact | 280 | -0.70c | -0.50c | 47% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 244 | +0.94c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2373 | +0.16c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 509 | -0.33c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2630 | -0.50c | +0.00c | 49% | NOISE (no measurable edge) |
| sports | 20 | -4.88c | -4.25c | 26% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 789 | +0.45c | -0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 834 | +0.11c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3534 | -0.30c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 619 | -0.57c | -0.00c | 57% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5275 | -0.16c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 501 | -0.22c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 435 | +0.90c | +0.10c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1040 | +0.21c | +0.05c | 53% | NOISE (no measurable edge) |
| over a month | 3750 | -0.18c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 428 | -1.64c | +0.00c | 50% | FADE (signal points the wrong way) |
| under 1 day | 49 | -5.26c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.42c | 45% |
| p_6h (alerted only) | 110 | -0.86c | 43% |
| p_24h (alerted only) | 85 | +1.78c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

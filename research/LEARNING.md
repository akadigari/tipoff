# What the scanner has learned about itself

_Auto-generated 2026-08-07T16:03:47Z. 10000 candidates logged, 5965 with a filled 24h forward price._

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
| alerted (passed gate and score) | 85 | -0.19c | +0.00c | 49% | NOISE (no measurable edge) |
| filtered out | 5642 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 238 | -0.69c | -0.00c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| cross_platform | 143 | +0.28c | +0.00c | 49% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4963 | -0.26c | -0.00c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 19 | -0.27c | +0.15c | 56% | INSUFFICIENT DATA |
| large_trade | 2068 | -0.33c | -0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1419 | -0.35c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 591 | -0.67c | +0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 1168 | -0.87c | -0.52c | 48% | NOISE (no measurable edge) |
| within_trader | 875 | -0.88c | -0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 43 | -1.03c | -0.00c | 49% | FADE (signal points the wrong way) |
| price_impact | 286 | -1.22c | -0.80c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2434 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 528 | -0.20c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 363 | -0.39c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2621 | -0.62c | +0.00c | 48% | NOISE (no measurable edge) |
| sports | 19 | -5.34c | -4.50c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 893 | -0.16c | +0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 839 | -0.24c | -0.00c | 50% | NOISE (no measurable edge) |
| under 40 | 3586 | -0.33c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 647 | -1.20c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5374 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 591 | -0.67c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 566 | +0.42c | +0.27c | 52% | NOISE (no measurable edge) |
| over a month | 3936 | -0.26c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 935 | -0.53c | -0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 394 | -2.18c | -0.20c | 48% | FADE (signal points the wrong way) |
| under 1 day | 38 | -4.34c | +0.03c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 113 | +0.49c | 46% |
| p_6h (alerted only) | 106 | -0.92c | 44% |
| p_24h (alerted only) | 85 | -0.19c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

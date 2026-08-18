# What the scanner has learned about itself

_Auto-generated 2026-08-18T03:04:35Z. 10000 candidates logged, 5597 with a filled 24h forward price._

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
| alerted (passed gate and score) | 52 | +0.58c | -0.07c | 48% | NOISE (no measurable edge) |
| filtered out | 5339 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 206 | -0.60c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 138 | +1.25c | -0.00c | 52% | FOLLOW |
| thin_market | 87 | +0.92c | +0.30c | 67% | NOISE (no measurable edge) |
| within_trader | 777 | +0.84c | +0.10c | 59% | NOISE (no measurable edge) |
| repeat_actor | 1281 | +0.51c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1816 | +0.51c | +0.00c | 57% | NOISE (no measurable edge) |
| volume_spike | 4901 | +0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 228 | +0.12c | -0.20c | 48% | NOISE (no measurable edge) |
| insiderable | 511 | -0.18c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.27c | -0.00c | 48% | NOISE (no measurable edge) |
| coordination | 7 | -0.37c | +0.30c | 67% | INSUFFICIENT DATA |
| price_jump | 818 | -0.69c | -0.45c | 48% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2571 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 622 | +0.16c | -0.00c | 53% | NOISE (no measurable edge) |
| other | 2262 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 128 | -0.58c | +0.00c | 50% | NOISE (no measurable edge) |
| sports | 14 | -3.50c | -0.75c | 38% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 820 | +0.38c | +0.00c | 56% | NOISE (no measurable edge) |
| 70+ | 558 | +0.22c | +0.00c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 773 | +0.05c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3446 | -0.02c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5086 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 511 | -0.18c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 78 | +1.36c | +0.23c | 54% | FOLLOW |
| 3 to 7 days | 391 | +0.98c | +0.20c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1216 | +0.45c | -0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3424 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 354 | -0.47c | +0.05c | 53% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 75 | +0.06c | 48% |
| p_6h (alerted only) | 70 | -0.20c | 45% |
| p_24h (alerted only) | 52 | +0.58c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

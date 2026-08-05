# What the scanner has learned about itself

_Auto-generated 2026-08-05T17:50:29Z. 10000 candidates logged, 5776 with a filled 24h forward price._

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
| filtered out | 5465 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 232 | -0.50c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 79 | -0.63c | -0.10c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| fresh_wallet | 18 | +0.57c | +0.40c | 59% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| cross_platform | 122 | -0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4778 | -0.31c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2056 | -0.43c | -0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1416 | -0.49c | +0.00c | 53% | NOISE (no measurable edge) |
| insiderable | 610 | -0.60c | -0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 288 | -0.64c | -0.50c | 47% | NOISE (no measurable edge) |
| price_jump | 1174 | -0.86c | -1.00c | 47% | NOISE (no measurable edge) |
| thin_market | 44 | -1.03c | +0.00c | 46% | FADE (signal points the wrong way) |
| within_trader | 861 | -1.05c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 516 | +0.33c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2292 | -0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 360 | -0.33c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2585 | -0.72c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 23 | -1.96c | -2.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3418 | -0.23c | +0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 880 | -0.37c | +0.00c | 53% | NOISE (no measurable edge) |
| 40 to 54 | 815 | -0.37c | -0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 663 | -1.14c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5166 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 610 | -0.60c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 557 | +0.47c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3774 | -0.24c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 916 | -0.52c | +0.00c | 49% | NOISE (no measurable edge) |
| under 1 day | 41 | -2.50c | +0.30c | 56% | FADE (signal points the wrong way) |
| 1 to 3 days | 384 | -2.67c | -0.50c | 46% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 100 | +0.25c | 42% |
| p_6h (alerted only) | 96 | -1.04c | 46% |
| p_24h (alerted only) | 79 | -0.63c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-05T19:49:09Z. 10000 candidates logged, 5807 with a filled 24h forward price._

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
| filtered out | 5497 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 79 | -0.48c | -0.10c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 231 | -0.62c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| fresh_wallet | 19 | +0.59c | +0.15c | 56% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| cross_platform | 125 | -0.08c | -0.00c | 48% | NOISE (no measurable edge) |
| volume_spike | 4802 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2057 | -0.43c | -0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1416 | -0.49c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 607 | -0.56c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 286 | -0.65c | -0.50c | 47% | NOISE (no measurable edge) |
| price_jump | 1184 | -0.83c | -1.00c | 47% | NOISE (no measurable edge) |
| thin_market | 43 | -1.04c | -0.00c | 47% | FADE (signal points the wrong way) |
| within_trader | 859 | -1.10c | -0.00c | 53% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 515 | +0.30c | -0.00c | 50% | NOISE (no measurable edge) |
| politics | 2307 | -0.12c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 361 | -0.34c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2602 | -0.72c | +0.00c | 48% | NOISE (no measurable edge) |
| sports | 22 | -1.82c | -2.00c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3446 | -0.23c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 825 | -0.35c | +0.00c | 49% | NOISE (no measurable edge) |
| 55 to 69 | 878 | -0.35c | -0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 658 | -1.16c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5200 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 607 | -0.56c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 558 | +0.48c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3803 | -0.25c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 914 | -0.47c | +0.00c | 50% | NOISE (no measurable edge) |
| under 1 day | 41 | -2.50c | +0.30c | 56% | FADE (signal points the wrong way) |
| 1 to 3 days | 387 | -2.60c | -0.35c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 102 | +0.29c | 42% |
| p_6h (alerted only) | 94 | -1.01c | 45% |
| p_24h (alerted only) | 79 | -0.48c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

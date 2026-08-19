# What the scanner has learned about itself

_Auto-generated 2026-08-19T21:34:33Z. 10000 candidates logged, 5227 with a filled 24h forward price._

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
| alerted (passed gate and score) | 40 | +0.10c | +0.22c | 53% | NOISE (no measurable edge) |
| filtered out | 5013 | -0.12c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 174 | -1.21c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| within_trader | 713 | +0.41c | -0.00c | 56% | NOISE (no measurable edge) |
| cross_platform | 123 | +0.40c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 207 | +0.23c | -0.55c | 45% | NOISE (no measurable edge) |
| coordination | 9 | +0.08c | +0.50c | 75% | INSUFFICIENT DATA |
| thin_market | 50 | +0.00c | +0.05c | 60% | NOISE (no measurable edge) |
| volume_spike | 4599 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1601 | -0.15c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1147 | -0.20c | +0.00c | 56% | NOISE (no measurable edge) |
| insiderable | 486 | -0.29c | +0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 26 | -0.34c | +0.02c | 55% | INSUFFICIENT DATA |
| price_jump | 720 | -1.40c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 695 | +0.55c | +0.05c | 55% | NOISE (no measurable edge) |
| politics | 2403 | -0.03c | -0.00c | 49% | NOISE (no measurable edge) |
| other | 2016 | -0.44c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 109 | -1.93c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 4 | -3.75c | -2.25c | 50% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3281 | -0.10c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 704 | -0.21c | +0.00c | 50% | NOISE (no measurable edge) |
| 55 to 69 | 744 | -0.26c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 498 | -0.26c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4741 | -0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 486 | -0.29c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 64 | +3.65c | +0.00c | 52% | FOLLOW |
| over a month | 3339 | -0.12c | +0.00c | 47% | NOISE (no measurable edge) |
| 3 to 7 days | 281 | -0.21c | +0.10c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1143 | -0.27c | -0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 268 | -0.70c | +0.05c | 52% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 79 | +1.20c | 54% |
| p_6h (alerted only) | 59 | +0.74c | 52% |
| p_24h (alerted only) | 40 | +0.10c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-27T19:02:39Z. 10000 candidates logged, 6438 with a filled 24h forward price._

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
| alerted (passed gate and score) | 64 | +0.62c | -0.50c | 47% | NOISE (no measurable edge) |
| filtered out | 6144 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 230 | -1.21c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 62 | +1.24c | +0.00c | 46% | FOLLOW |
| insiderable | 568 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 345 | +0.06c | -1.00c | 47% | NOISE (no measurable edge) |
| volume_spike | 5653 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 937 | -0.23c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 19 | -0.39c | -0.05c | 33% | INSUFFICIENT DATA |
| large_trade | 2157 | -0.46c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1588 | -0.63c | +0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 932 | -1.06c | -0.90c | 48% | FADE (signal points the wrong way) |
| coordination | 8 | -1.09c | +0.03c | 50% | INSUFFICIENT DATA |
| thin_market | 32 | -3.13c | +0.08c | 55% | FADE (signal points the wrong way) |
| chatter | 6 | -3.58c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2263 | -0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 1568 | -0.11c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2506 | -0.19c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 101 | -1.39c | -1.00c | 35% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 826 | +0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3861 | +0.09c | -0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 1015 | -0.63c | -0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 736 | -0.84c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 568 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| normal | 5870 | -0.15c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 539 | +0.50c | +0.25c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 278 | -0.00c | +0.72c | 53% | NOISE (no measurable edge) |
| over a month | 3975 | -0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1528 | -0.72c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 97 | +1.29c | 55% |
| p_6h (alerted only) | 87 | +3.09c | 55% |
| p_24h (alerted only) | 64 | +0.62c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

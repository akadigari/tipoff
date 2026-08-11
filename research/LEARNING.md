# What the scanner has learned about itself

_Auto-generated 2026-08-11T14:23:04Z. 10000 candidates logged, 5605 with a filled 24h forward price._

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
| alerted (passed gate and score) | 85 | +0.99c | +1.00c | 53% | NOISE (no measurable edge) |
| filtered out | 5278 | -0.14c | -0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 242 | -0.53c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 165 | +1.39c | +0.00c | 52% | FOLLOW |
| fresh_wallet | 21 | +0.82c | -0.10c | 45% | INSUFFICIENT DATA |
| thin_market | 70 | +0.76c | +0.20c | 61% | NOISE (no measurable edge) |
| repeat_actor | 1355 | +0.33c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1951 | +0.27c | +0.05c | 57% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4781 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 826 | -0.14c | +0.05c | 57% | NOISE (no measurable edge) |
| price_jump | 929 | -0.23c | -0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 487 | -0.41c | -0.00c | 46% | NOISE (no measurable edge) |
| price_impact | 262 | -1.20c | -0.50c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2294 | +0.10c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 201 | +0.09c | +0.00c | 45% | NOISE (no measurable edge) |
| crypto | 477 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2608 | -0.30c | +0.00c | 49% | NOISE (no measurable edge) |
| sports | 25 | -4.84c | -4.50c | 25% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 786 | +0.27c | +0.00c | 52% | NOISE (no measurable edge) |
| 55 to 69 | 824 | +0.27c | +0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3383 | -0.30c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 612 | -0.33c | +0.00c | 58% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5118 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 487 | -0.41c | -0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 367 | +1.40c | +0.45c | 58% | FOLLOW |
| 1 to 4 weeks | 1127 | +0.44c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3547 | -0.31c | -0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 423 | -1.28c | +0.05c | 51% | FADE (signal points the wrong way) |
| under 1 day | 61 | -4.09c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 116 | +0.42c | 47% |
| p_6h (alerted only) | 110 | -0.68c | 44% |
| p_24h (alerted only) | 85 | +0.99c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

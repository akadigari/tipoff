# What the scanner has learned about itself

_Auto-generated 2026-08-10T21:53:17Z. 10000 candidates logged, 5767 with a filled 24h forward price._

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
| alerted (passed gate and score) | 86 | +1.25c | +0.58c | 52% | FOLLOW |
| filtered out | 5434 | -0.18c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 247 | -0.56c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 166 | +1.52c | +0.00c | 54% | FOLLOW |
| fresh_wallet | 18 | +0.81c | -0.05c | 47% | INSUFFICIENT DATA |
| thin_market | 70 | +0.25c | +0.20c | 59% | NOISE (no measurable edge) |
| repeat_actor | 1386 | +0.21c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1974 | +0.16c | +0.05c | 56% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4885 | -0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 504 | -0.18c | -0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 848 | -0.20c | +0.05c | 57% | NOISE (no measurable edge) |
| price_jump | 991 | -0.43c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 274 | -1.07c | -0.50c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 233 | +0.69c | -0.00c | 48% | NOISE (no measurable edge) |
| politics | 2370 | +0.12c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2646 | -0.40c | -0.00c | 49% | NOISE (no measurable edge) |
| crypto | 496 | -0.51c | -0.05c | 44% | NOISE (no measurable edge) |
| sports | 22 | -5.23c | -5.00c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 775 | +0.63c | +0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 839 | +0.14c | -0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3519 | -0.36c | -0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 634 | -0.55c | +0.00c | 58% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5263 | -0.17c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 504 | -0.18c | -0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 405 | +1.15c | +0.40c | 55% | FOLLOW |
| 1 to 4 weeks | 1080 | +0.33c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3710 | -0.25c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 438 | -1.59c | +0.00c | 50% | FADE (signal points the wrong way) |
| under 1 day | 51 | -4.74c | +0.05c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 111 | +0.49c | 46% |
| p_6h (alerted only) | 109 | -0.81c | 43% |
| p_24h (alerted only) | 86 | +1.25c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

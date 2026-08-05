# What the scanner has learned about itself

_Auto-generated 2026-08-05T21:21:23Z. 10000 candidates logged, 5819 with a filled 24h forward price._

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
| alerted (passed gate and score) | 78 | -0.28c | -0.05c | 49% | NOISE (no measurable edge) |
| filtered out | 5508 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 233 | -0.62c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| fresh_wallet | 19 | +0.59c | +0.15c | 56% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| cross_platform | 130 | -0.07c | -0.00c | 47% | NOISE (no measurable edge) |
| volume_spike | 4817 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2061 | -0.37c | -0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1419 | -0.40c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 607 | -0.57c | -0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1180 | -0.82c | -0.50c | 47% | NOISE (no measurable edge) |
| price_impact | 285 | -0.93c | -0.50c | 46% | NOISE (no measurable edge) |
| thin_market | 43 | -1.04c | -0.00c | 47% | FADE (signal points the wrong way) |
| within_trader | 855 | -1.06c | -0.00c | 53% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 519 | +0.31c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2312 | -0.12c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 360 | -0.33c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2606 | -0.73c | +0.00c | 48% | NOISE (no measurable edge) |
| sports | 22 | -1.82c | -2.00c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3453 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 830 | -0.32c | +0.00c | 50% | NOISE (no measurable edge) |
| 55 to 69 | 880 | -0.34c | +0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 656 | -1.01c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5212 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 607 | -0.57c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 560 | +0.53c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3810 | -0.25c | -0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 922 | -0.56c | +0.00c | 50% | NOISE (no measurable edge) |
| under 1 day | 41 | -2.50c | +0.30c | 56% | FADE (signal points the wrong way) |
| 1 to 3 days | 382 | -2.59c | -0.28c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 102 | +0.29c | 42% |
| p_6h (alerted only) | 93 | -0.92c | 46% |
| p_24h (alerted only) | 78 | -0.28c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

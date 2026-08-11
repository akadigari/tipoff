# What the scanner has learned about itself

_Auto-generated 2026-08-11T19:15:10Z. 10000 candidates logged, 5743 with a filled 24h forward price._

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
| alerted (passed gate and score) | 84 | +1.11c | +0.58c | 52% | FOLLOW |
| filtered out | 5416 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 243 | -0.45c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 164 | +0.95c | +0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 22 | +0.92c | -0.05c | 48% | INSUFFICIENT DATA |
| thin_market | 68 | +0.85c | +0.37c | 63% | NOISE (no measurable edge) |
| repeat_actor | 1382 | +0.44c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1975 | +0.39c | +0.05c | 57% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| within_trader | 843 | +0.04c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4925 | +0.03c | +0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 930 | +0.01c | -0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 493 | -0.38c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 261 | -1.26c | -0.50c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2334 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 506 | +0.01c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2682 | -0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 195 | -0.57c | -0.05c | 43% | NOISE (no measurable edge) |
| sports | 26 | -4.67c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 832 | +0.50c | +0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 807 | +0.24c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3478 | -0.18c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 626 | -0.31c | -0.00c | 58% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5250 | -0.00c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 493 | -0.38c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 372 | +1.81c | +0.40c | 58% | FOLLOW |
| 1 to 4 weeks | 1211 | +0.51c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3608 | -0.28c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 405 | -0.73c | +0.10c | 52% | NOISE (no measurable edge) |
| under 1 day | 63 | -4.40c | +0.00c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 114 | +0.50c | 47% |
| p_6h (alerted only) | 112 | -1.04c | 42% |
| p_24h (alerted only) | 84 | +1.11c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

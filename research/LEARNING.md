# What the scanner has learned about itself

_Auto-generated 2026-08-13T09:21:06Z. 10000 candidates logged, 5764 with a filled 24h forward price._

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
| alerted (passed gate and score) | 85 | +0.73c | -0.00c | 50% | NOISE (no measurable edge) |
| filtered out | 5442 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 237 | -0.87c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 163 | +1.45c | +0.00c | 53% | FOLLOW |
| thin_market | 69 | +1.29c | +0.45c | 66% | FOLLOW |
| repeat_actor | 1415 | +0.69c | +0.10c | 57% | NOISE (no measurable edge) |
| fresh_wallet | 25 | +0.53c | -0.05c | 41% | INSUFFICIENT DATA |
| large_trade | 2002 | +0.50c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 837 | +0.38c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4967 | +0.19c | -0.00c | 50% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| price_jump | 907 | +0.01c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 523 | -0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 264 | -0.46c | -0.50c | 47% | NOISE (no measurable edge) |
| coordination | 5 | -1.15c | -0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2648 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2394 | +0.16c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 539 | +0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 154 | -1.16c | -0.00c | 43% | FADE (signal points the wrong way) |
| sports | 29 | -4.66c | -4.00c | 29% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 873 | +0.52c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 819 | +0.31c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 614 | +0.27c | +0.00c | 57% | NOISE (no measurable edge) |
| under 40 | 3458 | -0.10c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5241 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 523 | -0.23c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 388 | +1.39c | +0.33c | 57% | FOLLOW |
| 1 to 4 weeks | 1357 | +0.44c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3490 | -0.07c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 354 | -0.24c | +0.10c | 53% | NOISE (no measurable edge) |
| under 1 day | 68 | -1.78c | +0.62c | 54% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 115 | +0.38c | 48% |
| p_6h (alerted only) | 109 | -0.97c | 42% |
| p_24h (alerted only) | 85 | +0.73c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

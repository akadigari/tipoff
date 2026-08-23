# What the scanner has learned about itself

_Auto-generated 2026-08-23T16:36:36Z. 10000 candidates logged, 5770 with a filled 24h forward price._

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
| alerted (passed gate and score) | 53 | +1.44c | +0.45c | 55% | FOLLOW |
| filtered out | 5512 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 205 | -1.29c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 278 | +1.07c | +0.00c | 49% | FOLLOW |
| cross_platform | 94 | +1.06c | +0.00c | 52% | FOLLOW |
| volume_spike | 5111 | -0.09c | -0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 778 | -0.13c | -0.05c | 49% | NOISE (no measurable edge) |
| within_trader | 836 | -0.16c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 517 | -0.27c | -0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1829 | -0.64c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1343 | -0.75c | +0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.94c | -0.00c | 42% | INSUFFICIENT DATA |
| thin_market | 46 | -2.27c | +0.03c | 55% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1232 | +0.44c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2160 | +0.12c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2283 | -0.38c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 95 | -2.29c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3546 | +0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 734 | +0.12c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 615 | -0.43c | -0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 875 | -0.83c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5253 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 517 | -0.27c | -0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 41 | +6.64c | +0.00c | 49% | FOLLOW |
| 3 to 7 days | 246 | +0.91c | +0.23c | 53% | NOISE (no measurable edge) |
| over a month | 3604 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 295 | -0.32c | +0.15c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1436 | -0.57c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.43c | 58% |
| p_6h (alerted only) | 81 | +2.15c | 51% |
| p_24h (alerted only) | 53 | +1.44c | 55% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

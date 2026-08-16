# What the scanner has learned about itself

_Auto-generated 2026-08-16T14:32:50Z. 10000 candidates logged, 5773 with a filled 24h forward price._

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
| alerted (passed gate and score) | 65 | +0.76c | +0.45c | 52% | NOISE (no measurable edge) |
| filtered out | 5492 | +0.12c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 216 | -0.84c | -0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 150 | +1.15c | +0.00c | 53% | FOLLOW |
| thin_market | 69 | +1.09c | +0.30c | 68% | FOLLOW |
| within_trader | 795 | +0.95c | +0.05c | 59% | NOISE (no measurable edge) |
| repeat_actor | 1298 | +0.73c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1853 | +0.66c | +0.05c | 57% | NOISE (no measurable edge) |
| volume_spike | 5000 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 515 | +0.05c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 890 | -0.51c | -0.10c | 48% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 258 | -0.65c | -0.50c | 46% | NOISE (no measurable edge) |
| fresh_wallet | 29 | -1.00c | -0.05c | 42% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 615 | +0.32c | -0.00c | 53% | NOISE (no measurable edge) |
| other | 2406 | +0.10c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 130 | +0.09c | +0.00c | 44% | NOISE (no measurable edge) |
| politics | 2604 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| sports | 18 | -4.58c | -1.50c | 35% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 823 | +0.75c | +0.05c | 57% | NOISE (no measurable edge) |
| 70+ | 585 | +0.23c | -0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 793 | +0.18c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3572 | -0.10c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5258 | +0.10c | -0.00c | 50% | NOISE (no measurable edge) |
| high | 515 | +0.05c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 68 | +1.60c | +0.67c | 54% | FOLLOW |
| 3 to 7 days | 429 | +1.24c | +0.20c | 55% | FOLLOW |
| 1 to 3 days | 340 | +0.55c | +0.15c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1285 | +0.41c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3530 | -0.18c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +0.02c | 49% |
| p_6h (alerted only) | 88 | +0.15c | 45% |
| p_24h (alerted only) | 65 | +0.76c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-09T05:53:40Z. 10000 candidates logged, 5813 with a filled 24h forward price._

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
| alerted (passed gate and score) | 81 | +0.93c | +1.00c | 54% | NOISE (no measurable edge) |
| filtered out | 5493 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 239 | -0.88c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 153 | +0.28c | +0.00c | 51% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| fresh_wallet | 19 | +0.02c | +0.15c | 56% | INSUFFICIENT DATA |
| large_trade | 1981 | -0.22c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4868 | -0.23c | +0.00c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1368 | -0.28c | +0.05c | 55% | NOISE (no measurable edge) |
| coordination | 2 | -0.37c | -0.37c | 50% | INSUFFICIENT DATA |
| insiderable | 526 | -0.42c | +0.00c | 45% | NOISE (no measurable edge) |
| thin_market | 43 | -0.49c | -0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 1073 | -0.72c | -1.00c | 47% | NOISE (no measurable edge) |
| within_trader | 865 | -0.78c | +0.00c | 54% | NOISE (no measurable edge) |
| price_impact | 282 | -1.14c | -1.00c | 44% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 518 | -0.05c | +0.00c | 47% | NOISE (no measurable edge) |
| politics | 2357 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2610 | -0.55c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 311 | -0.61c | -0.15c | 45% | NOISE (no measurable edge) |
| sports | 17 | -5.97c | -5.50c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 865 | -0.03c | -0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 799 | -0.09c | +0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3531 | -0.37c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 618 | -1.08c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5287 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 526 | -0.42c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 526 | +0.04c | +0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3825 | -0.23c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 937 | -0.34c | +0.00c | 51% | NOISE (no measurable edge) |
| 1 to 3 days | 403 | -2.12c | -0.20c | 48% | FADE (signal points the wrong way) |
| under 1 day | 36 | -4.44c | +0.18c | 56% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 113 | +0.53c | 47% |
| p_6h (alerted only) | 111 | -0.76c | 45% |
| p_24h (alerted only) | 81 | +0.93c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

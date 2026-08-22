# What the scanner has learned about itself

_Auto-generated 2026-08-22T06:54:49Z. 10000 candidates logged, 5454 with a filled 24h forward price._

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
| alerted (passed gate and score) | 43 | +3.80c | +0.50c | 55% | FOLLOW |
| filtered out | 5233 | +0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 178 | -0.86c | -0.00c | 53% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 230 | +2.18c | +1.00c | 54% | FOLLOW |
| cross_platform | 102 | +0.90c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 720 | +0.18c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4825 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 744 | -0.18c | +0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 468 | -0.34c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1630 | -0.62c | -0.00c | 53% | NOISE (no measurable edge) |
| repeat_actor | 1192 | -0.73c | +0.00c | 55% | NOISE (no measurable edge) |
| thin_market | 42 | -0.75c | +0.08c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 19 | -0.90c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 990 | +0.91c | +0.25c | 57% | NOISE (no measurable edge) |
| politics | 2240 | +0.09c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2138 | -0.39c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 86 | -1.79c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3460 | +0.19c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 691 | +0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 520 | -0.11c | +0.00c | 56% | NOISE (no measurable edge) |
| 55 to 69 | 783 | -0.75c | -0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4986 | +0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 468 | -0.34c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 48 | +4.60c | +0.00c | 48% | FOLLOW |
| 1 to 3 days | 287 | +1.05c | +0.40c | 56% | FOLLOW |
| 3 to 7 days | 232 | +0.86c | +0.20c | 52% | NOISE (no measurable edge) |
| over a month | 3464 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1272 | -0.58c | +0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 85 | +1.76c | 58% |
| p_6h (alerted only) | 72 | +3.20c | 55% |
| p_24h (alerted only) | 43 | +3.80c | 55% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

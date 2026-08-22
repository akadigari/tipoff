# What the scanner has learned about itself

_Auto-generated 2026-08-22T17:29:58Z. 10000 candidates logged, 5575 with a filled 24h forward price._

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
| alerted (passed gate and score) | 43 | +2.67c | +0.50c | 55% | FOLLOW |
| filtered out | 5345 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 187 | -1.06c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 235 | +2.12c | +0.50c | 53% | FOLLOW |
| cross_platform | 98 | +0.94c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4949 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 746 | -0.08c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 770 | -0.23c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 471 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1703 | -0.65c | -0.00c | 52% | NOISE (no measurable edge) |
| thin_market | 40 | -0.79c | +0.08c | 58% | NOISE (no measurable edge) |
| repeat_actor | 1243 | -0.79c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 19 | -1.06c | -0.00c | 44% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1088 | +0.73c | +0.20c | 55% | NOISE (no measurable edge) |
| politics | 2197 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2208 | -0.40c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 82 | -2.11c | +0.00c | 44% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3507 | +0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 706 | +0.12c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 548 | -0.35c | +0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 814 | -0.77c | -0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5104 | +0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 471 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 42 | +4.89c | +0.00c | 44% | FOLLOW |
| 3 to 7 days | 234 | +1.10c | +0.27c | 53% | FOLLOW |
| 1 to 3 days | 290 | +0.55c | +0.40c | 56% | NOISE (no measurable edge) |
| over a month | 3519 | -0.03c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1334 | -0.60c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 85 | +1.60c | 56% |
| p_6h (alerted only) | 72 | +3.08c | 53% |
| p_24h (alerted only) | 43 | +2.67c | 55% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

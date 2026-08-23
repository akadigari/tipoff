# What the scanner has learned about itself

_Auto-generated 2026-08-23T18:42:37Z. 10000 candidates logged, 5718 with a filled 24h forward price._

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
| alerted (passed gate and score) | 52 | +1.46c | +0.43c | 54% | FOLLOW |
| filtered out | 5464 | -0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 202 | -1.30c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 93 | +1.08c | -0.00c | 53% | FOLLOW |
| price_impact | 271 | +1.07c | +0.00c | 49% | FOLLOW |
| price_jump | 773 | -0.06c | -0.10c | 49% | NOISE (no measurable edge) |
| volume_spike | 5068 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 829 | -0.18c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 512 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1823 | -0.65c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1338 | -0.78c | +0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 21 | -1.00c | -0.00c | 41% | INSUFFICIENT DATA |
| thin_market | 45 | -2.20c | +0.05c | 56% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1234 | +0.44c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2132 | +0.12c | -0.00c | 51% | NOISE (no measurable edge) |
| other | 2260 | -0.40c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 92 | -1.12c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3504 | +0.21c | +0.00c | 48% | NOISE (no measurable edge) |
| 40 to 54 | 733 | +0.10c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 612 | -0.43c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 869 | -0.86c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5206 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 512 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +5.71c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 242 | +0.95c | +0.25c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 303 | +0.16c | +0.25c | 55% | NOISE (no measurable edge) |
| over a month | 3560 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1428 | -0.59c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.29c | 58% |
| p_6h (alerted only) | 81 | +2.01c | 51% |
| p_24h (alerted only) | 52 | +1.46c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

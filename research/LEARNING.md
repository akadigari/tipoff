# What the scanner has learned about itself

_Auto-generated 2026-08-20T11:36:29Z. 10000 candidates logged, 5169 with a filled 24h forward price._

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
| filtered out | 4970 | -0.19c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 164 | -0.68c | -0.00c | 54% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 35 | -1.21c | +0.45c | 53% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 8 | +0.84c | +0.55c | 86% | INSUFFICIENT DATA |
| cross_platform | 118 | +0.58c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 697 | +0.38c | -0.00c | 56% | NOISE (no measurable edge) |
| large_trade | 1535 | -0.02c | +0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4528 | -0.03c | +0.00c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1101 | -0.10c | +0.05c | 57% | NOISE (no measurable edge) |
| thin_market | 46 | -0.19c | +0.08c | 64% | NOISE (no measurable edge) |
| insiderable | 462 | -0.39c | +0.00c | 50% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.45c | +0.05c | 55% | INSUFFICIENT DATA |
| price_impact | 212 | -0.57c | -0.60c | 45% | NOISE (no measurable edge) |
| price_jump | 702 | -1.77c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2427 | -0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 684 | -0.04c | +0.02c | 54% | NOISE (no measurable edge) |
| other | 1946 | -0.44c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 111 | -1.81c | +0.00c | 46% | FADE (signal points the wrong way) |
| sports | 1 | -13.50c | -13.50c | 0% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 470 | -0.18c | +0.00c | 55% | NOISE (no measurable edge) |
| under 40 | 3308 | -0.21c | +0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 718 | -0.24c | +0.00c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 673 | -0.26c | -0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4707 | -0.20c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 462 | -0.39c | +0.00c | 50% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 55 | +4.49c | +0.00c | 51% | FOLLOW |
| 3 to 7 days | 248 | -0.11c | +0.38c | 55% | NOISE (no measurable edge) |
| over a month | 3374 | -0.22c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1108 | -0.35c | +0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 253 | -1.80c | -0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 82 | +1.91c | 57% |
| p_6h (alerted only) | 65 | +3.21c | 56% |
| p_24h (alerted only) | 35 | -1.21c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

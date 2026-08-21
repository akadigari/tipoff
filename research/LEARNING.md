# What the scanner has learned about itself

_Auto-generated 2026-08-21T13:52:57Z. 10000 candidates logged, 5363 with a filled 24h forward price._

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
| alerted (passed gate and score) | 43 | +3.46c | +0.45c | 52% | FOLLOW |
| filtered out | 5149 | +0.02c | -0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 171 | -0.70c | +0.00c | 53% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 113 | +0.87c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 214 | +0.29c | -0.05c | 49% | NOISE (no measurable edge) |
| within_trader | 716 | +0.21c | +0.00c | 57% | NOISE (no measurable edge) |
| volume_spike | 4731 | +0.13c | -0.00c | 49% | NOISE (no measurable edge) |
| thin_market | 44 | -0.19c | +0.10c | 66% | NOISE (no measurable edge) |
| large_trade | 1599 | -0.23c | -0.00c | 55% | NOISE (no measurable edge) |
| coordination | 9 | -0.24c | +0.60c | 88% | INSUFFICIENT DATA |
| price_jump | 722 | -0.25c | -0.38c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1151 | -0.28c | +0.05c | 56% | NOISE (no measurable edge) |
| insiderable | 448 | -0.29c | +0.00c | 46% | NOISE (no measurable edge) |
| fresh_wallet | 22 | -0.47c | +0.05c | 58% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 885 | +0.91c | +0.20c | 57% | NOISE (no measurable edge) |
| politics | 2321 | -0.02c | -0.00c | 49% | NOISE (no measurable edge) |
| other | 2058 | -0.20c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 99 | -1.94c | -1.00c | 42% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 494 | +0.57c | +0.00c | 58% | NOISE (no measurable edge) |
| under 40 | 3424 | +0.11c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 676 | -0.05c | -0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 769 | -0.60c | -0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4915 | +0.06c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 448 | -0.29c | +0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 50 | +4.54c | +0.00c | 48% | FOLLOW |
| 3 to 7 days | 247 | +0.70c | +0.35c | 55% | NOISE (no measurable edge) |
| 1 to 3 days | 288 | +0.46c | +0.38c | 56% | NOISE (no measurable edge) |
| over a month | 3385 | -0.06c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1253 | -0.27c | +0.00c | 50% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 80 | +1.83c | 55% |
| p_6h (alerted only) | 68 | +3.33c | 55% |
| p_24h (alerted only) | 43 | +3.46c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

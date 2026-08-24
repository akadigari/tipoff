# What the scanner has learned about itself

_Auto-generated 2026-08-24T15:50:21Z. 10000 candidates logged, 5727 with a filled 24h forward price._

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
| filtered out | 5465 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 57 | -0.45c | -0.50c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 205 | -1.11c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 284 | +1.18c | +0.00c | 50% | FOLLOW |
| cross_platform | 91 | +1.01c | +0.00c | 49% | FOLLOW |
| within_trader | 848 | +0.04c | -0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 5058 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 526 | -0.10c | +0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 773 | -0.28c | -0.10c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.30c | -0.00c | 43% | INSUFFICIENT DATA |
| large_trade | 1875 | -0.54c | -0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1379 | -0.63c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 37 | -2.37c | -0.00c | 53% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1309 | +0.31c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2112 | +0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 93 | +0.01c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2213 | -0.45c | +0.00c | 45% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 743 | +0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3466 | +0.10c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 627 | -0.28c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 891 | -0.76c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5201 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 526 | -0.10c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +4.43c | +0.00c | 46% | FOLLOW |
| 3 to 7 days | 227 | +1.38c | +0.35c | 53% | FOLLOW |
| over a month | 3578 | +0.03c | -0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 276 | -0.30c | +0.50c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1481 | -0.63c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.32c | 58% |
| p_6h (alerted only) | 82 | +1.91c | 52% |
| p_24h (alerted only) | 57 | -0.45c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

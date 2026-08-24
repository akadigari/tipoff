# What the scanner has learned about itself

_Auto-generated 2026-08-24T13:57:34Z. 10000 candidates logged, 5784 with a filled 24h forward price._

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
| filtered out | 5520 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 57 | -0.27c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 207 | -1.11c | +0.00c | 52% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 282 | +1.12c | +0.00c | 50% | FOLLOW |
| cross_platform | 89 | +1.08c | +0.00c | 51% | FOLLOW |
| volume_spike | 5110 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 853 | -0.11c | -0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 534 | -0.14c | +0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.30c | -0.00c | 43% | INSUFFICIENT DATA |
| price_jump | 781 | -0.33c | -0.25c | 49% | NOISE (no measurable edge) |
| large_trade | 1888 | -0.59c | +0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1383 | -0.69c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 42 | -1.90c | -0.00c | 53% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1302 | +0.33c | +0.05c | 53% | NOISE (no measurable edge) |
| politics | 2136 | +0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2247 | -0.45c | -0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 99 | -0.82c | +0.00c | 46% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 751 | +0.23c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3507 | +0.12c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 629 | -0.33c | +0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 897 | -0.82c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5250 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 534 | -0.14c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 41 | +4.36c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 229 | +1.04c | +0.35c | 53% | FOLLOW |
| over a month | 3611 | +0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 292 | -0.29c | +0.40c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1481 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | +1.31c | 58% |
| p_6h (alerted only) | 83 | +1.89c | 51% |
| p_24h (alerted only) | 57 | -0.27c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

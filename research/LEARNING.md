# What the scanner has learned about itself

_Auto-generated 2026-08-23T23:30:24Z. 10000 candidates logged, 5753 with a filled 24h forward price._

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
| alerted (passed gate and score) | 54 | +0.92c | +0.43c | 54% | NOISE (no measurable edge) |
| filtered out | 5492 | -0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 207 | -1.14c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 91 | +1.10c | -0.00c | 53% | FOLLOW |
| price_impact | 271 | +1.07c | +0.00c | 49% | FOLLOW |
| volume_spike | 5102 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 849 | -0.13c | -0.00c | 55% | NOISE (no measurable edge) |
| price_jump | 770 | -0.20c | -0.05c | 49% | NOISE (no measurable edge) |
| insiderable | 528 | -0.22c | +0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 18 | -0.34c | +0.00c | 43% | INSUFFICIENT DATA |
| large_trade | 1849 | -0.59c | -0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1360 | -0.70c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 43 | -1.42c | +0.05c | 56% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1235 | +0.42c | +0.05c | 53% | NOISE (no measurable edge) |
| politics | 2143 | +0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2279 | -0.40c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 96 | -3.10c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3511 | +0.12c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 736 | +0.10c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 615 | -0.29c | +0.00c | 55% | NOISE (no measurable edge) |
| 55 to 69 | 891 | -0.80c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5225 | -0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 528 | -0.22c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +4.29c | +0.00c | 44% | FOLLOW |
| 3 to 7 days | 238 | +1.00c | +0.43c | 54% | FOLLOW |
| over a month | 3592 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 303 | -0.12c | +0.25c | 54% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1441 | -0.58c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.29c | 58% |
| p_6h (alerted only) | 83 | +1.78c | 50% |
| p_24h (alerted only) | 54 | +0.92c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

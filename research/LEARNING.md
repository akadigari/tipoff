# What the scanner has learned about itself

_Auto-generated 2026-08-23T20:34:24Z. 10000 candidates logged, 5764 with a filled 24h forward price._

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
| filtered out | 5506 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 206 | -1.27c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 273 | +1.11c | -0.10c | 49% | FOLLOW |
| cross_platform | 91 | +1.10c | -0.00c | 53% | FOLLOW |
| price_jump | 777 | -0.05c | -0.10c | 49% | NOISE (no measurable edge) |
| volume_spike | 5108 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 840 | -0.16c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 523 | -0.26c | +0.00c | 46% | NOISE (no measurable edge) |
| fresh_wallet | 19 | -0.31c | +0.00c | 47% | INSUFFICIENT DATA |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1837 | -0.63c | -0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1350 | -0.76c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 43 | -2.30c | -0.00c | 54% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1234 | +0.44c | +0.05c | 53% | NOISE (no measurable edge) |
| politics | 2151 | +0.12c | -0.00c | 51% | NOISE (no measurable edge) |
| other | 2285 | -0.39c | -0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 94 | -1.71c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3531 | +0.19c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 740 | +0.10c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 615 | -0.35c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 878 | -0.86c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5241 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 523 | -0.26c | +0.00c | 46% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 41 | +4.28c | -0.00c | 46% | FOLLOW |
| 3 to 7 days | 242 | +0.96c | +0.27c | 54% | NOISE (no measurable edge) |
| 1 to 3 days | 302 | +0.26c | +0.30c | 54% | NOISE (no measurable edge) |
| over a month | 3597 | -0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1439 | -0.58c | -0.00c | 48% | NOISE (no measurable edge) |

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

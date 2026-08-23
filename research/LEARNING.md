# What the scanner has learned about itself

_Auto-generated 2026-08-23T13:40:32Z. 10000 candidates logged, 5759 with a filled 24h forward price._

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
| alerted (passed gate and score) | 50 | +2.15c | +0.75c | 57% | FOLLOW |
| filtered out | 5510 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 199 | -0.96c | -0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 277 | +1.12c | +0.00c | 49% | FOLLOW |
| cross_platform | 94 | +1.06c | +0.00c | 52% | FOLLOW |
| volume_spike | 5099 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 770 | -0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 824 | -0.14c | -0.00c | 55% | NOISE (no measurable edge) |
| insiderable | 512 | -0.27c | +0.00c | 45% | NOISE (no measurable edge) |
| large_trade | 1802 | -0.59c | +0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| repeat_actor | 1325 | -0.70c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 45 | -0.78c | +0.05c | 56% | NOISE (no measurable edge) |
| fresh_wallet | 20 | -1.08c | +0.00c | 47% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1222 | +0.44c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2165 | +0.14c | -0.00c | 51% | NOISE (no measurable edge) |
| other | 2280 | -0.37c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 92 | -1.57c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3574 | +0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| 40 to 54 | 723 | +0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 603 | -0.37c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 859 | -0.72c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5247 | -0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 512 | -0.27c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +5.26c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 250 | +1.02c | +0.27c | 54% | FOLLOW |
| 1 to 3 days | 289 | +0.15c | +0.35c | 55% | NOISE (no measurable edge) |
| over a month | 3604 | -0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1425 | -0.56c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 92 | +1.46c | 58% |
| p_6h (alerted only) | 80 | +2.00c | 51% |
| p_24h (alerted only) | 50 | +2.15c | 57% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

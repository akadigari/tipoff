# What the scanner has learned about itself

_Auto-generated 2026-08-14T04:56:40Z. 10000 candidates logged, 5646 with a filled 24h forward price._

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
| alerted (passed gate and score) | 78 | +0.92c | +0.50c | 52% | NOISE (no measurable edge) |
| filtered out | 5346 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 222 | -0.90c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 1 | +2.00c | +2.00c | 100% | INSUFFICIENT DATA |
| thin_market | 68 | +1.68c | +0.47c | 68% | FOLLOW |
| cross_platform | 162 | +1.52c | +0.00c | 55% | FOLLOW |
| fresh_wallet | 25 | +0.96c | +0.00c | 45% | INSUFFICIENT DATA |
| large_trade | 1887 | +0.63c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 788 | +0.62c | +0.08c | 58% | NOISE (no measurable edge) |
| repeat_actor | 1325 | +0.62c | +0.10c | 57% | NOISE (no measurable edge) |
| volume_spike | 4854 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 490 | +0.10c | +0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 891 | -0.16c | -0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 261 | -0.30c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 4 | -1.26c | -0.03c | 33% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2421 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2524 | +0.20c | -0.00c | 51% | NOISE (no measurable edge) |
| crypto | 544 | +0.04c | +0.00c | 51% | NOISE (no measurable edge) |
| entertainment | 133 | -0.99c | +0.00c | 44% | NOISE (no measurable edge) |
| sports | 24 | -4.60c | -3.50c | 26% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 838 | +0.53c | -0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 800 | +0.44c | -0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 570 | +0.20c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3438 | -0.04c | +0.00c | 48% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5156 | +0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| high | 490 | +0.10c | +0.00c | 52% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 391 | +1.54c | +0.30c | 58% | FOLLOW |
| 1 to 4 weeks | 1337 | +0.40c | -0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 326 | +0.25c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3427 | -0.09c | +0.00c | 48% | NOISE (no measurable edge) |
| under 1 day | 68 | -0.60c | +0.67c | 56% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 110 | +0.16c | 44% |
| p_6h (alerted only) | 103 | -0.22c | 45% |
| p_24h (alerted only) | 78 | +0.92c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

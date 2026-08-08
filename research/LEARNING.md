# What the scanner has learned about itself

_Auto-generated 2026-08-08T18:52:19Z. 10000 candidates logged, 5733 with a filled 24h forward price._

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
| alerted (passed gate and score) | 80 | +1.02c | +0.75c | 54% | FOLLOW |
| filtered out | 5420 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 233 | -0.64c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.08c | +0.65c | 67% | INSUFFICIENT DATA |
| cross_platform | 149 | +0.17c | +0.00c | 49% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| repeat_actor | 1373 | -0.14c | +0.05c | 55% | NOISE (no measurable edge) |
| large_trade | 1991 | -0.14c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4789 | -0.23c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 531 | -0.26c | +0.00c | 47% | NOISE (no measurable edge) |
| fresh_wallet | 20 | -0.28c | +0.07c | 53% | INSUFFICIENT DATA |
| price_jump | 1085 | -0.55c | -0.50c | 48% | NOISE (no measurable edge) |
| price_impact | 273 | -0.73c | -0.85c | 45% | NOISE (no measurable edge) |
| within_trader | 851 | -0.77c | +0.00c | 55% | NOISE (no measurable edge) |
| thin_market | 42 | -1.10c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 503 | -0.05c | +0.00c | 47% | NOISE (no measurable edge) |
| politics | 2337 | -0.14c | -0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 319 | -0.16c | +0.00c | 46% | NOISE (no measurable edge) |
| other | 2557 | -0.50c | +0.00c | 49% | NOISE (no measurable edge) |
| sports | 17 | -5.85c | -5.50c | 19% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 867 | +0.01c | -0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 787 | -0.17c | -0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3454 | -0.32c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 625 | -0.91c | +0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 531 | -0.26c | +0.00c | 47% | NOISE (no measurable edge) |
| normal | 5202 | -0.32c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 552 | +0.27c | +0.17c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 886 | -0.13c | +0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3777 | -0.25c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 395 | -1.82c | -0.10c | 49% | FADE (signal points the wrong way) |
| under 1 day | 35 | -4.53c | +0.30c | 58% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 111 | +0.56c | 46% |
| p_6h (alerted only) | 105 | -0.77c | 45% |
| p_24h (alerted only) | 80 | +1.02c | 54% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

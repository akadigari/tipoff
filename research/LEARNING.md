# What the scanner has learned about itself

_Auto-generated 2026-08-13T20:55:39Z. 10000 candidates logged, 5698 with a filled 24h forward price._

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
| alerted (passed gate and score) | 80 | +0.25c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5388 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 230 | -0.86c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 159 | +1.54c | +0.00c | 53% | FOLLOW |
| thin_market | 65 | +1.53c | +0.30c | 65% | FOLLOW |
| fresh_wallet | 24 | +0.73c | -0.03c | 43% | INSUFFICIENT DATA |
| repeat_actor | 1367 | +0.71c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1939 | +0.58c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 812 | +0.49c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4903 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| price_jump | 907 | -0.08c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 509 | -0.10c | -0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 262 | -0.18c | -0.05c | 48% | NOISE (no measurable edge) |
| coordination | 5 | -1.29c | -0.05c | 25% | INSUFFICIENT DATA |
| chatter | 9 | -2.83c | +2.00c | 62% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2405 | +0.26c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2578 | +0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 555 | +0.01c | -0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 134 | -1.05c | +0.00c | 47% | FADE (signal points the wrong way) |
| sports | 26 | -4.88c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 853 | +0.50c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 809 | +0.48c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 598 | +0.22c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3438 | -0.06c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5189 | +0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 509 | -0.10c | -0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 394 | +1.49c | +0.30c | 57% | FOLLOW |
| 1 to 4 weeks | 1359 | +0.43c | -0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 346 | -0.02c | +0.10c | 53% | NOISE (no measurable edge) |
| over a month | 3427 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| under 1 day | 69 | -1.54c | +0.40c | 55% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 108 | +0.13c | 45% |
| p_6h (alerted only) | 103 | -0.74c | 43% |
| p_24h (alerted only) | 80 | +0.25c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

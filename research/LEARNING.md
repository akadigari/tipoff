# What the scanner has learned about itself

_Auto-generated 2026-08-10T23:45:59Z. 10000 candidates logged, 5773 with a filled 24h forward price._

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
| alerted (passed gate and score) | 87 | +1.17c | +0.15c | 52% | FOLLOW |
| filtered out | 5441 | -0.15c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 245 | -0.42c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 165 | +1.53c | +0.00c | 53% | FOLLOW |
| fresh_wallet | 19 | +0.76c | -0.10c | 44% | INSUFFICIENT DATA |
| repeat_actor | 1386 | +0.26c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1978 | +0.19c | +0.05c | 57% | NOISE (no measurable edge) |
| thin_market | 69 | +0.18c | -0.00c | 57% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4897 | -0.02c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 501 | -0.16c | +0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 850 | -0.18c | +0.05c | 57% | NOISE (no measurable edge) |
| price_jump | 988 | -0.30c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 271 | -1.12c | -0.75c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 226 | +0.68c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2367 | +0.12c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 497 | -0.35c | +0.00c | 44% | NOISE (no measurable edge) |
| other | 2661 | -0.37c | -0.00c | 49% | NOISE (no measurable edge) |
| sports | 22 | -5.23c | -5.00c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 781 | +0.59c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 838 | +0.24c | -0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3519 | -0.34c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 635 | -0.44c | +0.00c | 58% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5272 | -0.14c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 501 | -0.16c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 405 | +1.39c | +0.40c | 56% | FOLLOW |
| 1 to 4 weeks | 1097 | +0.39c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3697 | -0.26c | -0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 438 | -1.50c | +0.02c | 51% | FADE (signal points the wrong way) |
| under 1 day | 51 | -4.74c | +0.05c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 111 | +0.49c | 46% |
| p_6h (alerted only) | 110 | -0.80c | 43% |
| p_24h (alerted only) | 87 | +1.17c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

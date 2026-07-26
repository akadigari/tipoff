# What the scanner has learned about itself

_Auto-generated 2026-07-26T07:43:07Z. 10000 candidates logged, 5936 with a filled 24h forward price._

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
| filtered out | 5617 | -0.39c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 92 | -1.24c | -1.00c | 42% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 227 | -1.85c | -0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 5 | +2.02c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1130 | -0.06c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1815 | -0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 785 | -0.21c | -0.00c | 49% | NOISE (no measurable edge) |
| volume_spike | 4757 | -0.28c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 353 | -0.50c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 623 | -1.01c | -0.00c | 47% | FADE (signal points the wrong way) |
| price_jump | 1390 | -1.70c | -1.00c | 46% | FADE (signal points the wrong way) |
| cross_platform | 96 | -1.92c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 25 | -2.18c | -1.00c | 32% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 61 | +0.53c | +0.25c | 58% | NOISE (no measurable edge) |
| crypto | 624 | +0.19c | +0.00c | 52% | NOISE (no measurable edge) |
| other | 2800 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2093 | -0.56c | +0.00c | 43% | NOISE (no measurable edge) |
| entertainment | 358 | -1.03c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3668 | -0.33c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 797 | -0.42c | -0.00c | 49% | NOISE (no measurable edge) |
| 40 to 54 | 881 | -0.58c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 590 | -1.14c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5313 | -0.39c | -0.00c | 47% | NOISE (no measurable edge) |
| high | 623 | -1.01c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 19 | +3.18c | -0.50c | 47% | INSUFFICIENT DATA |
| 3 to 7 days | 261 | +0.61c | +0.60c | 56% | NOISE (no measurable edge) |
| 1 to 3 days | 221 | +0.22c | +0.15c | 50% | NOISE (no measurable edge) |
| over a month | 3558 | -0.48c | -0.00c | 45% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1789 | -0.69c | -0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 127 | -0.47c | 46% |
| p_6h (alerted only) | 120 | -1.15c | 46% |
| p_24h (alerted only) | 92 | -1.24c | 42% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-07-26T16:10:53Z. 10000 candidates logged, 5916 with a filled 24h forward price._

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
| filtered out | 5595 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 92 | -1.32c | -1.00c | 40% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 229 | -1.59c | -0.00c | 44% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 14 | +2.97c | -0.55c | 38% | INSUFFICIENT DATA |
| coordination | 4 | +2.53c | +2.75c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1174 | -0.08c | -0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1867 | -0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 796 | -0.22c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4741 | -0.27c | -0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 354 | -0.41c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 644 | -0.95c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1390 | -1.56c | -1.00c | 47% | FADE (signal points the wrong way) |
| cross_platform | 94 | -1.96c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 27 | -1.98c | -0.50c | 38% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 60 | +0.12c | +0.13c | 58% | NOISE (no measurable edge) |
| crypto | 628 | +0.02c | -0.00c | 52% | NOISE (no measurable edge) |
| other | 2791 | -0.39c | -0.00c | 49% | NOISE (no measurable edge) |
| politics | 2088 | -0.58c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 349 | -0.66c | +0.00c | 49% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 814 | -0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3602 | -0.32c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 889 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 611 | -1.12c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5272 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 644 | -0.95c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 17 | +5.70c | -0.50c | 47% | INSUFFICIENT DATA |
| 3 to 7 days | 288 | +0.97c | +1.00c | 59% | NOISE (no measurable edge) |
| 1 to 3 days | 225 | -0.07c | +0.25c | 51% | NOISE (no measurable edge) |
| over a month | 3523 | -0.42c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1772 | -0.75c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 126 | -0.39c | 47% |
| p_6h (alerted only) | 118 | -1.08c | 47% |
| p_24h (alerted only) | 92 | -1.32c | 40% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

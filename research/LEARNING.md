# What the scanner has learned about itself

_Auto-generated 2026-07-29T19:38:06Z. 10000 candidates logged, 5711 with a filled 24h forward price._

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
| filtered out | 5416 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 223 | -1.10c | +0.00c | 45% | FADE (signal points the wrong way) |
| alerted (passed gate and score) | 72 | -1.48c | -1.00c | 41% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 17 | +1.32c | -0.10c | 44% | INSUFFICIENT DATA |
| chatter | 4 | +1.19c | +0.58c | 75% | INSUFFICIENT DATA |
| repeat_actor | 1239 | -0.00c | -0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1883 | -0.10c | -0.00c | 52% | NOISE (no measurable edge) |
| price_impact | 326 | -0.14c | -0.50c | 47% | NOISE (no measurable edge) |
| within_trader | 824 | -0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4607 | -0.24c | -0.00c | 48% | NOISE (no measurable edge) |
| insiderable | 647 | -0.66c | +0.00c | 47% | NOISE (no measurable edge) |
| thin_market | 36 | -1.36c | -0.15c | 44% | FADE (signal points the wrong way) |
| price_jump | 1273 | -1.54c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 92 | -2.69c | +0.00c | 44% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 23 | +1.09c | -0.00c | 56% | INSUFFICIENT DATA |
| crypto | 560 | -0.13c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2116 | -0.41c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2614 | -0.43c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 398 | -0.56c | +0.00c | 48% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 839 | -0.08c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3449 | -0.31c | -0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 835 | -0.74c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 588 | -0.88c | +0.00c | 49% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5064 | -0.36c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 647 | -0.66c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 21 | +10.17c | +7.20c | 62% | INSUFFICIENT DATA |
| 1 to 3 days | 256 | +0.00c | +0.23c | 52% | NOISE (no measurable edge) |
| 3 to 7 days | 474 | -0.17c | +0.03c | 51% | NOISE (no measurable edge) |
| over a month | 3439 | -0.25c | -0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1427 | -1.03c | -0.05c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 103 | +0.24c | 47% |
| p_6h (alerted only) | 93 | -0.20c | 49% |
| p_24h (alerted only) | 72 | -1.48c | 41% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

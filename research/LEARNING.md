# What the scanner has learned about itself

_Auto-generated 2026-08-01T10:07:28Z. 10000 candidates logged, 5703 with a filled 24h forward price._

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
| alerted (passed gate and score) | 60 | +0.53c | -0.55c | 47% | NOISE (no measurable edge) |
| filtered out | 5427 | -0.41c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 216 | -1.38c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 13 | +2.80c | +2.00c | 62% | INSUFFICIENT DATA |
| coordination | 2 | +2.30c | +2.30c | 100% | INSUFFICIENT DATA |
| large_trade | 1971 | -0.22c | +0.00c | 53% | NOISE (no measurable edge) |
| volume_spike | 4678 | -0.29c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1317 | -0.35c | -0.00c | 53% | NOISE (no measurable edge) |
| insiderable | 632 | -0.44c | -0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 836 | -0.48c | +0.00c | 52% | NOISE (no measurable edge) |
| cross_platform | 96 | -0.80c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1207 | -1.31c | -1.00c | 47% | FADE (signal points the wrong way) |
| price_impact | 288 | -1.34c | -1.00c | 45% | FADE (signal points the wrong way) |
| thin_market | 40 | -1.46c | -0.40c | 37% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 15 | +1.20c | -0.00c | 50% | INSUFFICIENT DATA |
| entertainment | 378 | +0.39c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 555 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2191 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2564 | -0.76c | +0.00c | 48% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 852 | -0.17c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3414 | -0.33c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 818 | -0.56c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 619 | -1.22c | -0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5071 | -0.43c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 632 | -0.44c | -0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 27 | +5.21c | +1.95c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 548 | +0.41c | +0.27c | 52% | NOISE (no measurable edge) |
| over a month | 3589 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1112 | -1.04c | -0.00c | 48% | FADE (signal points the wrong way) |
| 1 to 3 days | 337 | -1.22c | -0.20c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 84 | +0.05c | 45% |
| p_6h (alerted only) | 79 | -0.27c | 47% |
| p_24h (alerted only) | 60 | +0.53c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-12T06:22:43Z. 10000 candidates logged, 5651 with a filled 24h forward price._

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
| alerted (passed gate and score) | 82 | +0.84c | +0.08c | 51% | NOISE (no measurable edge) |
| filtered out | 5324 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 245 | -1.00c | -0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 168 | +1.25c | +0.00c | 50% | FOLLOW |
| thin_market | 70 | +1.02c | +0.47c | 66% | FOLLOW |
| fresh_wallet | 21 | +0.82c | -0.10c | 45% | INSUFFICIENT DATA |
| repeat_actor | 1369 | +0.51c | +0.10c | 58% | NOISE (no measurable edge) |
| large_trade | 1938 | +0.44c | +0.10c | 57% | NOISE (no measurable edge) |
| within_trader | 829 | +0.25c | +0.10c | 59% | NOISE (no measurable edge) |
| price_jump | 879 | +0.23c | -0.00c | 50% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| coordination | 4 | +0.06c | +0.33c | 67% | INSUFFICIENT DATA |
| volume_spike | 4874 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| insiderable | 498 | -0.27c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 256 | -1.03c | -0.50c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2614 | +0.16c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2330 | -0.00c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 495 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 184 | -0.52c | -0.03c | 43% | NOISE (no measurable edge) |
| sports | 28 | -4.79c | -4.25c | 26% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 824 | +0.59c | +0.05c | 56% | NOISE (no measurable edge) |
| 40 to 54 | 793 | +0.47c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3424 | -0.13c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 610 | -0.42c | -0.00c | 57% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5153 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 498 | -0.27c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 371 | +1.70c | +0.30c | 57% | FOLLOW |
| 1 to 4 weeks | 1235 | +0.52c | +0.05c | 54% | NOISE (no measurable edge) |
| over a month | 3516 | -0.16c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 367 | -0.47c | +0.05c | 51% | NOISE (no measurable edge) |
| under 1 day | 71 | -3.10c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 116 | +0.12c | 48% |
| p_6h (alerted only) | 112 | -1.23c | 40% |
| p_24h (alerted only) | 82 | +0.84c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

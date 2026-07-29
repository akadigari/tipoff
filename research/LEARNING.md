# What the scanner has learned about itself

_Auto-generated 2026-07-29T21:08:22Z. 10000 candidates logged, 5686 with a filled 24h forward price._

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
| filtered out | 5393 | -0.39c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 71 | -0.72c | -1.00c | 43% | NOISE (no measurable edge) |
| monitor (strong but gated) | 222 | -1.11c | +0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 16 | +1.46c | -0.05c | 47% | INSUFFICIENT DATA |
| repeat_actor | 1248 | -0.03c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1889 | -0.12c | +0.00c | 52% | NOISE (no measurable edge) |
| price_impact | 323 | -0.16c | -0.50c | 48% | NOISE (no measurable edge) |
| volume_spike | 4594 | -0.24c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 828 | -0.26c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 642 | -0.73c | +0.00c | 47% | NOISE (no measurable edge) |
| thin_market | 36 | -1.36c | -0.15c | 44% | FADE (signal points the wrong way) |
| price_jump | 1262 | -1.59c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 92 | -2.69c | +0.00c | 44% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 22 | +1.14c | +0.00c | 56% | INSUFFICIENT DATA |
| crypto | 559 | -0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2105 | -0.44c | +0.00c | 45% | NOISE (no measurable edge) |
| other | 2606 | -0.45c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 394 | -0.57c | +0.00c | 48% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 847 | -0.07c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3428 | -0.35c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 824 | -0.78c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 587 | -0.86c | -0.00c | 49% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5044 | -0.38c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 642 | -0.73c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 21 | +10.17c | +7.20c | 62% | INSUFFICIENT DATA |
| 1 to 3 days | 260 | +0.12c | +0.15c | 52% | NOISE (no measurable edge) |
| 3 to 7 days | 482 | -0.20c | +0.00c | 50% | NOISE (no measurable edge) |
| over a month | 3416 | -0.27c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1413 | -1.09c | -0.05c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 101 | +0.22c | 48% |
| p_6h (alerted only) | 90 | +0.02c | 51% |
| p_24h (alerted only) | 71 | -0.72c | 43% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

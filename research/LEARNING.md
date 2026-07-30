# What the scanner has learned about itself

_Auto-generated 2026-07-30T19:45:21Z. 10000 candidates logged, 5734 with a filled 24h forward price._

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
| filtered out | 5441 | -0.46c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 68 | -0.86c | -1.25c | 43% | NOISE (no measurable edge) |
| monitor (strong but gated) | 225 | -1.23c | -0.00c | 46% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 14 | +1.53c | -0.05c | 46% | INSUFFICIENT DATA |
| repeat_actor | 1295 | -0.09c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1932 | -0.16c | +0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4645 | -0.26c | -0.00c | 48% | NOISE (no measurable edge) |
| insiderable | 641 | -0.45c | -0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 837 | -0.49c | -0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 316 | -0.82c | -1.00c | 46% | NOISE (no measurable edge) |
| thin_market | 38 | -1.43c | -0.35c | 39% | FADE (signal points the wrong way) |
| cross_platform | 95 | -1.53c | +0.00c | 47% | FADE (signal points the wrong way) |
| price_jump | 1276 | -1.73c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 21 | +1.19c | +0.00c | 56% | INSUFFICIENT DATA |
| entertainment | 382 | +0.20c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 548 | -0.24c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2156 | -0.33c | +0.00c | 46% | NOISE (no measurable edge) |
| other | 2627 | -0.80c | +0.00c | 47% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 857 | -0.23c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3437 | -0.43c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 614 | -0.79c | +0.00c | 50% | NOISE (no measurable edge) |
| 40 to 54 | 826 | -0.80c | +0.00c | 48% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 641 | -0.45c | -0.00c | 49% | NOISE (no measurable edge) |
| normal | 5093 | -0.50c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 20 | +10.31c | +5.68c | 60% | INSUFFICIENT DATA |
| 3 to 7 days | 518 | -0.02c | +0.10c | 51% | NOISE (no measurable edge) |
| over a month | 3483 | -0.34c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1305 | -1.06c | -0.05c | 47% | FADE (signal points the wrong way) |
| 1 to 3 days | 314 | -1.25c | -0.33c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 89 | +0.25c | 47% |
| p_6h (alerted only) | 84 | +0.14c | 52% |
| p_24h (alerted only) | 68 | -0.86c | 43% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

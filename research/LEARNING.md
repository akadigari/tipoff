# What the scanner has learned about itself

_Auto-generated 2026-08-03T04:38:46Z. 10000 candidates logged, 5840 with a filled 24h forward price._

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
| filtered out | 5548 | -0.45c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 64 | -0.50c | -1.25c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 228 | -0.71c | +0.00c | 45% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 15 | +2.37c | +0.65c | 60% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 11 | +0.79c | +2.00c | 73% | INSUFFICIENT DATA |
| large_trade | 2057 | -0.30c | -0.00c | 54% | NOISE (no measurable edge) |
| volume_spike | 4833 | -0.30c | -0.00c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1418 | -0.33c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 633 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 849 | -0.78c | -0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 113 | -0.87c | -0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 1193 | -1.23c | -1.00c | 47% | FADE (signal points the wrong way) |
| price_impact | 282 | -1.27c | -1.00c | 46% | FADE (signal points the wrong way) |
| thin_market | 46 | -1.90c | -0.30c | 38% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 379 | +0.21c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 557 | -0.03c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2271 | -0.28c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2613 | -0.80c | -0.00c | 47% | NOISE (no measurable edge) |
| sports | 20 | -0.93c | -0.25c | 41% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 880 | -0.24c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3476 | -0.35c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 824 | -0.64c | +0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 660 | -1.10c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5207 | -0.44c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 633 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 25 | +4.49c | +1.95c | 57% | INSUFFICIENT DATA |
| 3 to 7 days | 554 | +0.25c | +0.27c | 52% | NOISE (no measurable edge) |
| over a month | 3790 | -0.35c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1000 | -0.77c | +0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 373 | -1.95c | -0.20c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 87 | +0.77c | 44% |
| p_6h (alerted only) | 79 | -1.02c | 44% |
| p_24h (alerted only) | 64 | -0.50c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

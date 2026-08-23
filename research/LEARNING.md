# What the scanner has learned about itself

_Auto-generated 2026-08-23T05:38:21Z. 10000 candidates logged, 5780 with a filled 24h forward price._

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
| alerted (passed gate and score) | 49 | +2.28c | +1.00c | 58% | FOLLOW |
| filtered out | 5534 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 197 | -0.92c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 271 | +1.26c | -0.00c | 50% | FOLLOW |
| cross_platform | 94 | +1.06c | +0.00c | 51% | FOLLOW |
| volume_spike | 5124 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| price_jump | 778 | -0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 819 | -0.17c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 513 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1788 | -0.60c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1318 | -0.72c | +0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 44 | -0.76c | +0.05c | 57% | NOISE (no measurable edge) |
| fresh_wallet | 20 | -1.08c | +0.00c | 47% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1211 | +0.51c | +0.10c | 53% | NOISE (no measurable edge) |
| politics | 2203 | +0.10c | -0.00c | 51% | NOISE (no measurable edge) |
| other | 2273 | -0.36c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 93 | -1.92c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 724 | +0.17c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3601 | +0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 602 | -0.38c | -0.00c | 54% | NOISE (no measurable edge) |
| 55 to 69 | 853 | -0.75c | -0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5267 | -0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 513 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +5.26c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 255 | +0.97c | +0.25c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 292 | +0.18c | +0.38c | 56% | NOISE (no measurable edge) |
| over a month | 3614 | +0.00c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1421 | -0.57c | +0.00c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 89 | +1.44c | 57% |
| p_6h (alerted only) | 78 | +2.46c | 51% |
| p_24h (alerted only) | 49 | +2.28c | 58% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

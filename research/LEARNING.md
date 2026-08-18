# What the scanner has learned about itself

_Auto-generated 2026-08-18T18:51:31Z. 10000 candidates logged, 5511 with a filled 24h forward price._

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
| filtered out | 5282 | -0.04c | -0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 41 | -0.65c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 188 | -0.65c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 68 | +0.84c | +0.20c | 68% | NOISE (no measurable edge) |
| within_trader | 757 | +0.67c | +0.05c | 59% | NOISE (no measurable edge) |
| large_trade | 1764 | +0.22c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1242 | +0.18c | +0.05c | 56% | NOISE (no measurable edge) |
| volume_spike | 4840 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| coordination | 8 | +0.04c | +0.40c | 71% | INSUFFICIENT DATA |
| price_impact | 219 | +0.03c | -0.50c | 47% | NOISE (no measurable edge) |
| cross_platform | 131 | +0.03c | -0.00c | 46% | NOISE (no measurable edge) |
| insiderable | 501 | -0.21c | -0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.22c | -0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 777 | -1.17c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 673 | +0.38c | -0.00c | 55% | NOISE (no measurable edge) |
| politics | 2497 | -0.04c | -0.00c | 50% | NOISE (no measurable edge) |
| other | 2219 | -0.16c | -0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 109 | -1.12c | -0.00c | 49% | FADE (signal points the wrong way) |
| sports | 13 | -3.77c | -1.00c | 38% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 806 | +0.16c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 544 | +0.15c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3409 | -0.09c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 752 | -0.35c | -0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5010 | -0.05c | -0.00c | 49% | NOISE (no measurable edge) |
| high | 501 | -0.21c | -0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 77 | +2.30c | +0.00c | 53% | FOLLOW |
| 3 to 7 days | 347 | +0.87c | +0.30c | 56% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1230 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| over a month | 3415 | -0.15c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 301 | -1.16c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 71 | -0.24c | 45% |
| p_6h (alerted only) | 59 | -0.61c | 44% |
| p_24h (alerted only) | 41 | -0.65c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

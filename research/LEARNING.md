# What the scanner has learned about itself

_Auto-generated 2026-08-01T19:30:31Z. 10000 candidates logged, 5691 with a filled 24h forward price._

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
| alerted (passed gate and score) | 58 | +0.87c | +0.20c | 50% | NOISE (no measurable edge) |
| filtered out | 5415 | -0.47c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 218 | -1.12c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 13 | +2.80c | +2.00c | 62% | INSUFFICIENT DATA |
| coordination | 2 | +2.30c | +2.30c | 100% | INSUFFICIENT DATA |
| large_trade | 1972 | -0.25c | +0.00c | 53% | NOISE (no measurable edge) |
| volume_spike | 4674 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1330 | -0.39c | -0.00c | 53% | NOISE (no measurable edge) |
| insiderable | 622 | -0.48c | -0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 837 | -0.55c | +0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 99 | -0.77c | -0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 284 | -1.39c | -1.00c | 45% | FADE (signal points the wrong way) |
| price_jump | 1200 | -1.39c | -1.00c | 47% | FADE (signal points the wrong way) |
| thin_market | 42 | -1.86c | -0.47c | 35% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 15 | +0.40c | -0.00c | 42% | INSUFFICIENT DATA |
| entertainment | 379 | +0.39c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 549 | -0.09c | -0.00c | 50% | NOISE (no measurable edge) |
| politics | 2193 | -0.31c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2555 | -0.86c | -0.00c | 47% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 850 | -0.09c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3406 | -0.40c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 809 | -0.63c | -0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 626 | -1.28c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 622 | -0.48c | -0.00c | 47% | NOISE (no measurable edge) |
| normal | 5069 | -0.49c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 27 | +5.21c | +1.95c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 549 | +0.28c | +0.20c | 52% | NOISE (no measurable edge) |
| over a month | 3627 | -0.40c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1064 | -0.98c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 338 | -1.37c | -0.13c | 49% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 84 | +0.09c | 44% |
| p_6h (alerted only) | 78 | -0.62c | 46% |
| p_24h (alerted only) | 58 | +0.87c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

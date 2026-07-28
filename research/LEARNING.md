# What the scanner has learned about itself

_Auto-generated 2026-07-28T03:28:16Z. 10000 candidates logged, 5901 with a filled 24h forward price._

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
| filtered out | 5581 | -0.44c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 83 | -0.96c | -1.00c | 42% | NOISE (no measurable edge) |
| monitor (strong but gated) | 237 | -1.75c | -0.00c | 41% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 17 | +1.38c | -0.10c | 44% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1245 | +0.10c | -0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1921 | -0.02c | -0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 842 | -0.04c | +0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4715 | -0.29c | +0.00c | 47% | NOISE (no measurable edge) |
| insiderable | 664 | -0.94c | +0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 354 | -1.28c | -1.00c | 46% | FADE (signal points the wrong way) |
| thin_market | 31 | -1.44c | -0.50c | 41% | FADE (signal points the wrong way) |
| price_jump | 1370 | -1.77c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 91 | -2.91c | -0.15c | 39% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 614 | -0.33c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2728 | -0.37c | -0.00c | 49% | NOISE (no measurable edge) |
| sports | 45 | -0.54c | +0.00c | 56% | NOISE (no measurable edge) |
| politics | 2117 | -0.57c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 397 | -1.20c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 849 | -0.19c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3562 | -0.40c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 887 | -0.81c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 603 | -1.04c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5237 | -0.44c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 664 | -0.94c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 20 | +9.76c | +5.52c | 60% | INSUFFICIENT DATA |
| 3 to 7 days | 377 | +0.53c | +0.50c | 56% | NOISE (no measurable edge) |
| 1 to 3 days | 246 | +0.22c | +0.40c | 52% | NOISE (no measurable edge) |
| over a month | 3518 | -0.50c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1633 | -0.99c | -0.05c | 47% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 115 | -0.04c | 46% |
| p_6h (alerted only) | 107 | -0.20c | 48% |
| p_24h (alerted only) | 83 | -0.96c | 42% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

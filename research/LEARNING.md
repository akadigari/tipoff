# What the scanner has learned about itself

_Auto-generated 2026-08-03T19:50:28Z. 10000 candidates logged, 5840 with a filled 24h forward price._

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
| alerted (passed gate and score) | 67 | +0.10c | -0.20c | 47% | NOISE (no measurable edge) |
| filtered out | 5541 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 232 | -0.65c | +0.00c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 17 | +2.08c | +0.15c | 56% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 13 | +0.82c | +2.00c | 75% | INSUFFICIENT DATA |
| volume_spike | 4813 | -0.28c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2046 | -0.30c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1413 | -0.32c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 634 | -0.62c | +0.00c | 47% | NOISE (no measurable edge) |
| cross_platform | 113 | -0.72c | -0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 851 | -0.83c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 1215 | -0.84c | -0.55c | 47% | NOISE (no measurable edge) |
| price_impact | 278 | -0.96c | -0.92c | 46% | NOISE (no measurable edge) |
| thin_market | 44 | -1.97c | -0.30c | 38% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 533 | +0.37c | -0.00c | 52% | NOISE (no measurable edge) |
| politics | 2302 | -0.26c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 374 | -0.36c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2609 | -0.61c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 22 | -1.43c | -0.75c | 37% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 869 | -0.18c | -0.00c | 54% | NOISE (no measurable edge) |
| under 40 | 3479 | -0.25c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 835 | -0.58c | -0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 657 | -0.99c | -0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5206 | -0.34c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 634 | -0.62c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 557 | +0.44c | +0.30c | 52% | NOISE (no measurable edge) |
| over a month | 3799 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 973 | -0.46c | +0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 382 | -1.54c | -0.23c | 48% | FADE (signal points the wrong way) |
| under 1 day | 29 | -3.69c | +0.00c | 48% | INSUFFICIENT DATA |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 94 | +0.51c | 42% |
| p_6h (alerted only) | 86 | -0.92c | 44% |
| p_24h (alerted only) | 67 | +0.10c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

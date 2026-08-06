# What the scanner has learned about itself

_Auto-generated 2026-08-06T13:01:29Z. 10000 candidates logged, 5896 with a filled 24h forward price._

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
| filtered out | 5585 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 77 | -0.64c | -0.20c | 47% | NOISE (no measurable edge) |
| monitor (strong but gated) | 234 | -0.69c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| fresh_wallet | 19 | +0.59c | +0.15c | 56% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| cross_platform | 136 | -0.08c | -0.00c | 46% | NOISE (no measurable edge) |
| volume_spike | 4892 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2058 | -0.35c | -0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1422 | -0.36c | -0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 598 | -0.63c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1173 | -0.83c | -0.55c | 47% | NOISE (no measurable edge) |
| thin_market | 44 | -1.01c | -0.00c | 49% | FADE (signal points the wrong way) |
| within_trader | 860 | -1.02c | -0.00c | 53% | FADE (signal points the wrong way) |
| price_impact | 288 | -1.17c | -0.92c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 522 | +0.22c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2374 | -0.14c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 366 | -0.39c | +0.00c | 47% | NOISE (no measurable edge) |
| other | 2615 | -0.70c | +0.00c | 48% | NOISE (no measurable edge) |
| sports | 19 | -3.26c | -3.00c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3525 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 887 | -0.35c | -0.00c | 53% | NOISE (no measurable edge) |
| 40 to 54 | 844 | -0.36c | -0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 640 | -1.02c | +0.00c | 53% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5298 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 598 | -0.63c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 557 | +0.50c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3890 | -0.26c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 926 | -0.46c | +0.00c | 50% | NOISE (no measurable edge) |
| under 1 day | 40 | -2.61c | +0.18c | 55% | FADE (signal points the wrong way) |
| 1 to 3 days | 384 | -2.63c | -0.33c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 103 | +0.35c | 43% |
| p_6h (alerted only) | 99 | -0.92c | 45% |
| p_24h (alerted only) | 77 | -0.64c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

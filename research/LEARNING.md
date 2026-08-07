# What the scanner has learned about itself

_Auto-generated 2026-08-07T14:17:03Z. 10000 candidates logged, 5958 with a filled 24h forward price._

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
| alerted (passed gate and score) | 83 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| filtered out | 5639 | -0.39c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 236 | -0.63c | -0.00c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| cross_platform | 142 | +0.26c | +0.00c | 48% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4950 | -0.26c | +0.00c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 19 | -0.27c | +0.15c | 56% | INSUFFICIENT DATA |
| large_trade | 2052 | -0.35c | -0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1410 | -0.40c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 592 | -0.64c | -0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1170 | -0.92c | -1.00c | 47% | NOISE (no measurable edge) |
| within_trader | 867 | -0.93c | -0.00c | 54% | NOISE (no measurable edge) |
| thin_market | 43 | -1.03c | -0.00c | 49% | FADE (signal points the wrong way) |
| price_impact | 287 | -1.36c | -0.85c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2437 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 520 | -0.20c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 368 | -0.39c | +0.00c | 46% | NOISE (no measurable edge) |
| other | 2614 | -0.64c | +0.00c | 48% | NOISE (no measurable edge) |
| sports | 19 | -5.34c | -4.50c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 890 | -0.18c | +0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 834 | -0.32c | -0.00c | 50% | NOISE (no measurable edge) |
| under 40 | 3595 | -0.32c | -0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 639 | -1.19c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5366 | -0.37c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 592 | -0.64c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 562 | +0.46c | +0.27c | 52% | NOISE (no measurable edge) |
| over a month | 3936 | -0.26c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 931 | -0.58c | -0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 395 | -2.28c | -0.20c | 48% | FADE (signal points the wrong way) |
| under 1 day | 38 | -4.34c | +0.03c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.50c | 47% |
| p_6h (alerted only) | 106 | -0.92c | 44% |
| p_24h (alerted only) | 83 | -0.11c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

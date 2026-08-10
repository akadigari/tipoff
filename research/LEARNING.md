# What the scanner has learned about itself

_Auto-generated 2026-08-10T04:47:24Z. 10000 candidates logged, 5793 with a filled 24h forward price._

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
| alerted (passed gate and score) | 88 | +1.63c | +0.75c | 53% | FOLLOW |
| filtered out | 5460 | -0.21c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 245 | -0.57c | -0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 166 | +1.48c | +0.00c | 55% | FOLLOW |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| thin_market | 60 | +0.03c | +0.00c | 57% | NOISE (no measurable edge) |
| repeat_actor | 1358 | -0.03c | +0.05c | 56% | NOISE (no measurable edge) |
| price_impact | 282 | -0.06c | -0.30c | 48% | NOISE (no measurable edge) |
| large_trade | 1957 | -0.11c | -0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4886 | -0.12c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 507 | -0.32c | +0.00c | 44% | NOISE (no measurable edge) |
| price_jump | 1029 | -0.32c | -0.00c | 49% | NOISE (no measurable edge) |
| coordination | 2 | -0.37c | -0.37c | 50% | INSUFFICIENT DATA |
| within_trader | 851 | -0.54c | -0.00c | 55% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.56c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 259 | +0.45c | -0.00c | 48% | NOISE (no measurable edge) |
| politics | 2415 | +0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 502 | -0.30c | +0.00c | 46% | NOISE (no measurable edge) |
| other | 2599 | -0.54c | -0.00c | 48% | NOISE (no measurable edge) |
| sports | 18 | -5.64c | -5.00c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 794 | +0.29c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 845 | -0.06c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3539 | -0.27c | +0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 615 | -0.63c | -0.00c | 55% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5286 | -0.19c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 507 | -0.32c | +0.00c | 44% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 462 | +0.29c | +0.03c | 51% | NOISE (no measurable edge) |
| 1 to 4 weeks | 989 | +0.25c | +0.10c | 54% | NOISE (no measurable edge) |
| over a month | 3795 | -0.16c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 426 | -1.63c | +0.00c | 50% | FADE (signal points the wrong way) |
| under 1 day | 48 | -6.22c | +0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.39c | 45% |
| p_6h (alerted only) | 110 | -0.75c | 45% |
| p_24h (alerted only) | 88 | +1.63c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

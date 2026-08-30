# What the scanner has learned about itself

_Auto-generated 2026-08-30T08:14:58Z. 10000 candidates logged, 6516 with a filled 24h forward price._

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
| alerted (passed gate and score) | 66 | +1.44c | +0.00c | 49% | FOLLOW |
| filtered out | 6217 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 233 | -1.13c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 74 | +1.04c | +0.00c | 44% | FOLLOW |
| fresh_wallet | 22 | +0.39c | +0.00c | 44% | INSUFFICIENT DATA |
| price_impact | 348 | +0.15c | -0.68c | 48% | NOISE (no measurable edge) |
| insiderable | 577 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 5721 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 947 | -0.18c | +0.00c | 54% | NOISE (no measurable edge) |
| large_trade | 2194 | -0.34c | +0.00c | 52% | NOISE (no measurable edge) |
| repeat_actor | 1605 | -0.52c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 931 | -0.91c | -0.50c | 49% | NOISE (no measurable edge) |
| coordination | 7 | -1.34c | -0.20c | 43% | INSUFFICIENT DATA |
| thin_market | 34 | -2.81c | +0.08c | 56% | FADE (signal points the wrong way) |
| chatter | 6 | -3.58c | +0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2324 | +0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 1547 | -0.13c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2536 | -0.13c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 109 | -1.52c | -1.00c | 37% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 850 | +0.15c | +0.00c | 48% | NOISE (no measurable edge) |
| under 40 | 3897 | +0.08c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 1027 | -0.50c | -0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 742 | -0.78c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 577 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| normal | 5939 | -0.12c | -0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +9.67c | +19.30c | 61% | INSUFFICIENT DATA |
| 3 to 7 days | 560 | +0.67c | +0.30c | 55% | NOISE (no measurable edge) |
| over a month | 4072 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 284 | -0.09c | +0.85c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1482 | -0.72c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 98 | +1.17c | 56% |
| p_6h (alerted only) | 90 | +2.86c | 55% |
| p_24h (alerted only) | 66 | +1.44c | 49% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

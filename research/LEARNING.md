# What the scanner has learned about itself

_Auto-generated 2026-08-18T14:44:42Z. 10000 candidates logged, 5607 with a filled 24h forward price._

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
| filtered out | 5368 | +0.05c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 195 | -0.51c | -0.00c | 51% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 44 | -0.95c | -0.20c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 133 | +0.72c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 772 | +0.70c | +0.05c | 58% | NOISE (no measurable edge) |
| thin_market | 77 | +0.68c | +0.10c | 67% | NOISE (no measurable edge) |
| price_impact | 227 | +0.53c | -0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1261 | +0.30c | +0.05c | 57% | NOISE (no measurable edge) |
| large_trade | 1797 | +0.30c | -0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4922 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| coordination | 8 | +0.04c | +0.40c | 71% | INSUFFICIENT DATA |
| insiderable | 510 | -0.16c | +0.00c | 52% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.22c | -0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 795 | -0.90c | -0.55c | 47% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 654 | +0.35c | +0.00c | 54% | NOISE (no measurable edge) |
| politics | 2566 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2255 | -0.09c | -0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 118 | -0.16c | +0.00c | 51% | NOISE (no measurable edge) |
| sports | 14 | -3.50c | -0.75c | 38% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 819 | +0.28c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 557 | +0.23c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3474 | -0.03c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 757 | -0.18c | -0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5097 | +0.04c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 510 | -0.16c | +0.00c | 52% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 77 | +1.89c | +0.15c | 53% | FOLLOW |
| 3 to 7 days | 363 | +0.85c | +0.25c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1243 | +0.23c | -0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3463 | -0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 321 | -0.50c | +0.05c | 53% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 66 | -0.19c | 46% |
| p_6h (alerted only) | 62 | -0.61c | 43% |
| p_24h (alerted only) | 44 | -0.95c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

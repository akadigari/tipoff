# What the scanner has learned about itself

_Auto-generated 2026-08-12T21:56:22Z. 10000 candidates logged, 5662 with a filled 24h forward price._

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
| alerted (passed gate and score) | 86 | +0.93c | +0.08c | 52% | NOISE (no measurable edge) |
| filtered out | 5339 | +0.05c | +0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 237 | -0.72c | -0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 160 | +1.35c | +0.00c | 51% | FOLLOW |
| thin_market | 69 | +1.01c | +0.45c | 65% | FOLLOW |
| fresh_wallet | 24 | +0.69c | -0.03c | 43% | INSUFFICIENT DATA |
| repeat_actor | 1401 | +0.65c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1977 | +0.46c | +0.05c | 56% | NOISE (no measurable edge) |
| within_trader | 825 | +0.32c | +0.05c | 58% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4896 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 873 | -0.09c | -0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 253 | -0.28c | -0.50c | 47% | NOISE (no measurable edge) |
| insiderable | 507 | -0.44c | +0.00c | 49% | NOISE (no measurable edge) |
| coordination | 5 | -1.15c | -0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2312 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2622 | +0.12c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 536 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 161 | -1.16c | -0.05c | 42% | FADE (signal points the wrong way) |
| sports | 31 | -4.85c | -4.50c | 27% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 854 | +0.53c | +0.00c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 805 | +0.26c | +0.00c | 53% | NOISE (no measurable edge) |
| 70+ | 603 | +0.18c | +0.00c | 57% | NOISE (no measurable edge) |
| under 40 | 3400 | -0.17c | +0.00c | 46% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5155 | +0.08c | -0.00c | 50% | NOISE (no measurable edge) |
| high | 507 | -0.44c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 379 | +1.34c | +0.25c | 56% | FOLLOW |
| 1 to 4 weeks | 1331 | +0.38c | +0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3427 | -0.14c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 360 | -0.23c | +0.10c | 53% | NOISE (no measurable edge) |
| under 1 day | 66 | -1.97c | +0.25c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 117 | +0.29c | 48% |
| p_6h (alerted only) | 110 | -1.36c | 41% |
| p_24h (alerted only) | 86 | +0.93c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-05T03:25:35Z. 10000 candidates logged, 5768 with a filled 24h forward price._

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
| alerted (passed gate and score) | 74 | -0.02c | -0.15c | 47% | NOISE (no measurable edge) |
| filtered out | 5461 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 233 | -0.63c | -0.00c | 47% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 18 | +2.54c | +0.40c | 59% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| cross_platform | 125 | -0.09c | -0.00c | 49% | NOISE (no measurable edge) |
| volume_spike | 4775 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2033 | -0.41c | +0.00c | 53% | NOISE (no measurable edge) |
| repeat_actor | 1410 | -0.45c | -0.00c | 53% | NOISE (no measurable edge) |
| price_impact | 287 | -0.52c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 608 | -0.65c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 859 | -0.82c | +0.00c | 54% | NOISE (no measurable edge) |
| price_jump | 1165 | -1.05c | -1.00c | 46% | FADE (signal points the wrong way) |
| thin_market | 44 | -1.40c | -0.02c | 43% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 509 | +0.25c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2308 | -0.12c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 368 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2559 | -0.73c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 24 | -1.88c | -2.00c | 33% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3433 | -0.22c | -0.00c | 45% | NOISE (no measurable edge) |
| 55 to 69 | 866 | -0.37c | +0.00c | 53% | NOISE (no measurable edge) |
| 40 to 54 | 809 | -0.57c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 660 | -0.95c | +0.00c | 52% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5160 | -0.34c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 608 | -0.65c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 550 | +0.45c | +0.35c | 53% | NOISE (no measurable edge) |
| over a month | 3779 | -0.28c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 910 | -0.63c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 389 | -1.90c | -0.30c | 47% | FADE (signal points the wrong way) |
| under 1 day | 41 | -2.50c | +0.30c | 56% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 100 | +0.37c | 42% |
| p_6h (alerted only) | 97 | -1.04c | 45% |
| p_24h (alerted only) | 74 | -0.02c | 47% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

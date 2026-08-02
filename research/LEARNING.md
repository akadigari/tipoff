# What the scanner has learned about itself

_Auto-generated 2026-08-02T10:05:43Z. 10000 candidates logged, 5727 with a filled 24h forward price._

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
| alerted (passed gate and score) | 63 | +1.30c | +0.50c | 51% | FOLLOW |
| filtered out | 5448 | -0.48c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 216 | -0.74c | +0.00c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 14 | +2.61c | +1.32c | 64% | INSUFFICIENT DATA |
| coordination | 3 | +1.75c | +0.65c | 100% | INSUFFICIENT DATA |
| large_trade | 1991 | -0.25c | -0.00c | 53% | NOISE (no measurable edge) |
| volume_spike | 4712 | -0.31c | +0.00c | 48% | NOISE (no measurable edge) |
| insiderable | 622 | -0.34c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1358 | -0.46c | -0.00c | 53% | NOISE (no measurable edge) |
| within_trader | 822 | -0.72c | +0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 106 | -0.80c | +0.00c | 49% | NOISE (no measurable edge) |
| thin_market | 43 | -1.25c | -0.45c | 37% | FADE (signal points the wrong way) |
| price_jump | 1203 | -1.31c | -1.00c | 47% | FADE (signal points the wrong way) |
| price_impact | 290 | -1.43c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 386 | +0.21c | +0.00c | 51% | NOISE (no measurable edge) |
| sports | 18 | -0.11c | -0.00c | 47% | INSUFFICIENT DATA |
| crypto | 540 | -0.13c | -0.00c | 50% | NOISE (no measurable edge) |
| politics | 2212 | -0.29c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2571 | -0.80c | -0.00c | 48% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 860 | -0.15c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3415 | -0.38c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 817 | -0.52c | +0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 635 | -1.30c | +0.00c | 51% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 622 | -0.34c | +0.00c | 48% | NOISE (no measurable edge) |
| normal | 5105 | -0.49c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 25 | +1.21c | +0.00c | 52% | INSUFFICIENT DATA |
| 3 to 7 days | 549 | +0.21c | +0.20c | 52% | NOISE (no measurable edge) |
| over a month | 3684 | -0.37c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1043 | -0.95c | -0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 336 | -1.26c | -0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 85 | +0.20c | 46% |
| p_6h (alerted only) | 80 | -0.82c | 45% |
| p_24h (alerted only) | 63 | +1.30c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

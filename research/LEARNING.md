# What the scanner has learned about itself

_Auto-generated 2026-07-25T23:07:01Z. 10000 candidates logged, 5931 with a filled 24h forward price._

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
| filtered out | 5610 | -0.41c | +0.00c | 47% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 96 | -1.43c | -1.00c | 41% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 225 | -1.86c | -0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 4 | +1.52c | +1.55c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| within_trader | 774 | -0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| repeat_actor | 1112 | -0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| large_trade | 1800 | -0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4757 | -0.26c | -0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 352 | -0.82c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 618 | -0.91c | +0.00c | 47% | NOISE (no measurable edge) |
| thin_market | 22 | -1.69c | -0.75c | 35% | INSUFFICIENT DATA |
| price_jump | 1400 | -1.82c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 94 | -1.98c | +0.00c | 41% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 61 | +0.53c | +0.25c | 58% | NOISE (no measurable edge) |
| crypto | 636 | -0.28c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2811 | -0.46c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2070 | -0.49c | -0.00c | 43% | NOISE (no measurable edge) |
| entertainment | 353 | -1.16c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 795 | -0.34c | -0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3671 | -0.38c | -0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 873 | -0.65c | -0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 592 | -1.10c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5313 | -0.43c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 618 | -0.91c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 20 | +3.03c | -0.20c | 50% | INSUFFICIENT DATA |
| 3 to 7 days | 244 | +0.71c | +0.65c | 56% | NOISE (no measurable edge) |
| 1 to 3 days | 218 | -0.43c | -0.30c | 49% | NOISE (no measurable edge) |
| over a month | 3546 | -0.49c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1816 | -0.73c | -0.00c | 49% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 130 | -0.48c | 46% |
| p_6h (alerted only) | 122 | -1.12c | 47% |
| p_24h (alerted only) | 96 | -1.43c | 41% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

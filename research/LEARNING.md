# What the scanner has learned about itself

_Auto-generated 2026-08-18T23:30:56Z. 10000 candidates logged, 5487 with a filled 24h forward price._

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
| filtered out | 5259 | -0.06c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 42 | -0.77c | +0.22c | 52% | NOISE (no measurable edge) |
| monitor (strong but gated) | 186 | -0.80c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 59 | +0.86c | +0.30c | 69% | NOISE (no measurable edge) |
| within_trader | 759 | +0.57c | +0.05c | 58% | NOISE (no measurable edge) |
| large_trade | 1742 | +0.19c | +0.00c | 56% | NOISE (no measurable edge) |
| repeat_actor | 1235 | +0.17c | +0.05c | 57% | NOISE (no measurable edge) |
| coordination | 10 | +0.11c | +0.40c | 75% | INSUFFICIENT DATA |
| cross_platform | 133 | +0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| volume_spike | 4839 | +0.04c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 210 | +0.03c | -0.50c | 46% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.04c | +0.05c | 56% | NOISE (no measurable edge) |
| insiderable | 501 | -0.23c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 753 | -1.27c | -1.00c | 45% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 662 | +0.44c | +0.05c | 56% | NOISE (no measurable edge) |
| politics | 2534 | -0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2174 | -0.17c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 106 | -1.74c | +0.00c | 49% | FADE (signal points the wrong way) |
| sports | 11 | -4.82c | -6.00c | 27% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 796 | +0.17c | -0.00c | 56% | NOISE (no measurable edge) |
| 70+ | 546 | +0.06c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3397 | -0.12c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 748 | -0.35c | -0.00c | 51% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4986 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 501 | -0.23c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 77 | +1.46c | +0.00c | 49% | FOLLOW |
| 3 to 7 days | 345 | +0.65c | +0.25c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1211 | +0.13c | +0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3425 | -0.15c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 294 | -1.22c | +0.00c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 69 | -0.23c | 45% |
| p_6h (alerted only) | 62 | -0.27c | 46% |
| p_24h (alerted only) | 42 | -0.77c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

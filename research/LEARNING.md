# What the scanner has learned about itself

_Auto-generated 2026-08-19T03:06:45Z. 10000 candidates logged, 5469 with a filled 24h forward price._

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
| filtered out | 5242 | -0.07c | +0.00c | 49% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 42 | -0.70c | +0.22c | 52% | NOISE (no measurable edge) |
| monitor (strong but gated) | 185 | -0.87c | +0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 56 | +0.69c | +0.10c | 67% | NOISE (no measurable edge) |
| within_trader | 750 | +0.45c | -0.00c | 57% | NOISE (no measurable edge) |
| coordination | 10 | +0.11c | +0.40c | 75% | INSUFFICIENT DATA |
| large_trade | 1728 | +0.07c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1231 | +0.07c | +0.05c | 56% | NOISE (no measurable edge) |
| cross_platform | 137 | +0.06c | -0.00c | 47% | NOISE (no measurable edge) |
| volume_spike | 4820 | +0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| price_impact | 209 | -0.02c | -0.50c | 46% | NOISE (no measurable edge) |
| fresh_wallet | 31 | -0.04c | +0.05c | 56% | NOISE (no measurable edge) |
| insiderable | 500 | -0.32c | +0.00c | 52% | NOISE (no measurable edge) |
| price_jump | 755 | -1.02c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 668 | +0.45c | +0.05c | 56% | NOISE (no measurable edge) |
| politics | 2521 | -0.11c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2163 | -0.14c | -0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 106 | -1.87c | +0.00c | 48% | FADE (signal points the wrong way) |
| sports | 11 | -4.82c | -6.00c | 27% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 791 | +0.12c | +0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 542 | -0.04c | +0.00c | 55% | NOISE (no measurable edge) |
| under 40 | 3386 | -0.09c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 750 | -0.42c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4969 | -0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 500 | -0.32c | +0.00c | 52% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 76 | +1.30c | +0.00c | 49% | FOLLOW |
| 3 to 7 days | 331 | +0.47c | +0.20c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1207 | +0.12c | -0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3431 | -0.12c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 287 | -1.33c | +0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 67 | -0.10c | 47% |
| p_6h (alerted only) | 61 | -0.35c | 46% |
| p_24h (alerted only) | 42 | -0.70c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

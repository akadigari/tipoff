# What the scanner has learned about itself

_Auto-generated 2026-08-26T04:50:37Z. 10000 candidates logged, 5686 with a filled 24h forward price._

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
| alerted (passed gate and score) | 58 | +0.19c | -0.50c | 46% | NOISE (no measurable edge) |
| filtered out | 5419 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 209 | -1.08c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 61 | +1.21c | +0.00c | 42% | FOLLOW |
| price_impact | 307 | +0.39c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 510 | +0.01c | +0.00c | 47% | NOISE (no measurable edge) |
| volume_spike | 4984 | -0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 838 | -0.20c | +0.00c | 53% | NOISE (no measurable edge) |
| fresh_wallet | 13 | -0.45c | -0.05c | 30% | INSUFFICIENT DATA |
| large_trade | 1898 | -0.49c | +0.00c | 51% | NOISE (no measurable edge) |
| price_jump | 816 | -0.59c | -0.38c | 49% | NOISE (no measurable edge) |
| repeat_actor | 1397 | -0.66c | +0.00c | 52% | NOISE (no measurable edge) |
| coordination | 7 | -1.13c | +0.25c | 57% | INSUFFICIENT DATA |
| thin_market | 34 | -2.81c | +0.00c | 50% | FADE (signal points the wrong way) |
| chatter | 1 | -3.50c | -3.50c | 0% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1407 | +0.03c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 1984 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2199 | -0.15c | -0.00c | 46% | NOISE (no measurable edge) |
| entertainment | 96 | -1.04c | -1.00c | 36% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 743 | +0.21c | +0.00c | 49% | NOISE (no measurable edge) |
| under 40 | 3410 | +0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| 55 to 69 | 892 | -0.54c | +0.00c | 52% | NOISE (no measurable edge) |
| 70+ | 641 | -0.72c | +0.00c | 49% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| high | 510 | +0.01c | +0.00c | 47% | NOISE (no measurable edge) |
| normal | 5176 | -0.09c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 19 | +9.12c | +16.80c | 58% | INSUFFICIENT DATA |
| 3 to 7 days | 254 | +1.57c | +0.03c | 51% | FOLLOW |
| over a month | 3527 | -0.01c | -0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 249 | -0.25c | +0.75c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1529 | -0.72c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 93 | +1.01c | 54% |
| p_6h (alerted only) | 82 | +2.83c | 55% |
| p_24h (alerted only) | 58 | +0.19c | 46% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

# What the scanner has learned about itself

_Auto-generated 2026-08-13T17:08:36Z. 10000 candidates logged, 5703 with a filled 24h forward price._

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
| filtered out | 5391 | +0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 81 | -0.07c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 231 | -0.84c | +0.00c | 49% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 164 | +1.50c | +0.00c | 54% | FOLLOW |
| thin_market | 68 | +0.95c | +0.37c | 66% | NOISE (no measurable edge) |
| repeat_actor | 1373 | +0.70c | +0.15c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 25 | +0.66c | -0.05c | 41% | INSUFFICIENT DATA |
| large_trade | 1946 | +0.52c | +0.05c | 57% | NOISE (no measurable edge) |
| within_trader | 826 | +0.49c | +0.05c | 58% | NOISE (no measurable edge) |
| volume_spike | 4916 | +0.22c | +0.00c | 51% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| price_jump | 901 | -0.06c | -0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 506 | -0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| price_impact | 258 | -0.45c | -0.50c | 47% | NOISE (no measurable edge) |
| coordination | 4 | -1.60c | -0.70c | 33% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2393 | +0.20c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2588 | +0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 558 | -0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 138 | -1.18c | +0.00c | 44% | FADE (signal points the wrong way) |
| sports | 26 | -4.88c | -4.25c | 24% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 851 | +0.44c | +0.05c | 55% | NOISE (no measurable edge) |
| 40 to 54 | 810 | +0.38c | +0.00c | 54% | NOISE (no measurable edge) |
| 70+ | 602 | +0.37c | +0.00c | 57% | NOISE (no measurable edge) |
| under 40 | 3440 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5197 | +0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 506 | -0.19c | +0.00c | 51% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 389 | +1.47c | +0.35c | 57% | FOLLOW |
| 1 to 4 weeks | 1356 | +0.48c | -0.00c | 53% | NOISE (no measurable edge) |
| over a month | 3436 | -0.06c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 352 | -0.36c | +0.05c | 52% | NOISE (no measurable edge) |
| under 1 day | 67 | -1.19c | +0.95c | 55% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 110 | +0.29c | 46% |
| p_6h (alerted only) | 104 | -0.66c | 44% |
| p_24h (alerted only) | 81 | -0.07c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

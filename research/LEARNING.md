# What the scanner has learned about itself

_Auto-generated 2026-08-14T17:59:31Z. 10000 candidates logged, 5551 with a filled 24h forward price._

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
| alerted (passed gate and score) | 74 | +0.53c | +1.00c | 53% | NOISE (no measurable edge) |
| filtered out | 5263 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| monitor (strong but gated) | 214 | -1.08c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| thin_market | 70 | +1.65c | +0.47c | 68% | FOLLOW |
| cross_platform | 160 | +1.53c | +0.00c | 54% | FOLLOW |
| within_trader | 764 | +0.86c | +0.10c | 60% | NOISE (no measurable edge) |
| repeat_actor | 1301 | +0.78c | +0.15c | 59% | NOISE (no measurable edge) |
| large_trade | 1859 | +0.70c | +0.10c | 58% | NOISE (no measurable edge) |
| fresh_wallet | 24 | +0.57c | +0.00c | 50% | INSUFFICIENT DATA |
| volume_spike | 4792 | +0.24c | +0.00c | 51% | NOISE (no measurable edge) |
| insiderable | 477 | +0.10c | +0.00c | 53% | NOISE (no measurable edge) |
| price_jump | 866 | -0.24c | -0.00c | 51% | NOISE (no measurable edge) |
| coordination | 6 | -0.52c | +0.15c | 60% | INSUFFICIENT DATA |
| price_impact | 256 | -0.70c | -0.50c | 45% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 123 | +0.25c | -0.00c | 42% | NOISE (no measurable edge) |
| crypto | 571 | +0.22c | +0.00c | 52% | NOISE (no measurable edge) |
| politics | 2401 | +0.18c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2434 | +0.10c | +0.00c | 52% | NOISE (no measurable edge) |
| sports | 22 | -4.43c | -3.00c | 29% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 829 | +0.72c | +0.05c | 57% | NOISE (no measurable edge) |
| 40 to 54 | 782 | +0.33c | -0.00c | 55% | NOISE (no measurable edge) |
| 70+ | 564 | +0.27c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3376 | -0.08c | +0.00c | 47% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5074 | +0.14c | +0.00c | 51% | NOISE (no measurable edge) |
| high | 477 | +0.10c | +0.00c | 53% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 65 | +1.64c | +1.00c | 58% | FOLLOW |
| 3 to 7 days | 404 | +1.54c | +0.33c | 57% | FOLLOW |
| 1 to 4 weeks | 1299 | +0.42c | +0.05c | 54% | NOISE (no measurable edge) |
| over a month | 3365 | -0.07c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 319 | -0.22c | +0.10c | 54% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 106 | +0.17c | 45% |
| p_6h (alerted only) | 101 | -0.27c | 45% |
| p_24h (alerted only) | 74 | +0.53c | 53% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

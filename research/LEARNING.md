# What the scanner has learned about itself

_Auto-generated 2026-07-27T04:46:52Z. 10000 candidates logged, 5962 with a filled 24h forward price._

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
| filtered out | 5639 | -0.43c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 87 | -1.09c | -1.00c | 42% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 236 | -1.51c | +0.00c | 44% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 16 | +3.23c | -0.05c | 47% | INSUFFICIENT DATA |
| coordination | 4 | +2.53c | +2.75c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1215 | +0.03c | -0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1899 | -0.11c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 818 | -0.16c | -0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4786 | -0.29c | +0.00c | 48% | NOISE (no measurable edge) |
| insiderable | 655 | -0.87c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 352 | -1.09c | -0.50c | 48% | FADE (signal points the wrong way) |
| price_jump | 1397 | -1.66c | -1.00c | 46% | FADE (signal points the wrong way) |
| thin_market | 28 | -1.80c | -0.55c | 38% | INSUFFICIENT DATA |
| cross_platform | 99 | -2.26c | +0.00c | 40% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 633 | -0.14c | -0.00c | 52% | NOISE (no measurable edge) |
| sports | 57 | -0.22c | +0.25c | 59% | NOISE (no measurable edge) |
| other | 2771 | -0.45c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2130 | -0.55c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 371 | -1.02c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 836 | -0.13c | -0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3610 | -0.42c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 893 | -0.64c | -0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 623 | -1.12c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5307 | -0.44c | -0.00c | 48% | NOISE (no measurable edge) |
| high | 655 | -0.87c | +0.00c | 49% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +4.16c | -0.83c | 44% | INSUFFICIENT DATA |
| 3 to 7 days | 320 | +0.85c | +0.65c | 57% | NOISE (no measurable edge) |
| 1 to 3 days | 237 | -0.15c | +0.15c | 51% | NOISE (no measurable edge) |
| over a month | 3558 | -0.48c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1731 | -0.87c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 121 | -0.16c | 47% |
| p_6h (alerted only) | 112 | -0.61c | 47% |
| p_24h (alerted only) | 87 | -1.09c | 42% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

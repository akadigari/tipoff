# What the scanner has learned about itself

_Auto-generated 2026-07-26T18:09:03Z. 10000 candidates logged, 5899 with a filled 24h forward price._

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
| filtered out | 5578 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 90 | -1.33c | -1.00c | 40% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 231 | -1.59c | -0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 14 | +2.97c | -0.55c | 38% | INSUFFICIENT DATA |
| coordination | 4 | +2.53c | +2.75c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1177 | -0.06c | -0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1864 | -0.16c | +0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 798 | -0.20c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4726 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 351 | -0.46c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 637 | -0.94c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1391 | -1.58c | -1.00c | 46% | FADE (signal points the wrong way) |
| cross_platform | 94 | -1.96c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 27 | -1.98c | -0.50c | 38% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 632 | +0.03c | +0.00c | 53% | NOISE (no measurable edge) |
| sports | 58 | -0.29c | +0.13c | 58% | NOISE (no measurable edge) |
| entertainment | 351 | -0.41c | +0.00c | 50% | NOISE (no measurable edge) |
| other | 2778 | -0.43c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2080 | -0.59c | +0.00c | 44% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 814 | -0.23c | +0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3586 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 884 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 615 | -1.10c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5262 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 637 | -0.94c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 17 | +5.70c | -0.50c | 47% | INSUFFICIENT DATA |
| 3 to 7 days | 293 | +0.94c | +0.80c | 58% | NOISE (no measurable edge) |
| 1 to 3 days | 228 | -0.04c | +0.28c | 51% | NOISE (no measurable edge) |
| over a month | 3507 | -0.42c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1763 | -0.79c | -0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 124 | -0.42c | 47% |
| p_6h (alerted only) | 116 | -1.12c | 46% |
| p_24h (alerted only) | 90 | -1.33c | 40% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

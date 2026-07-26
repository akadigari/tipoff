# What the scanner has learned about itself

_Auto-generated 2026-07-26T14:42:46Z. 10000 candidates logged, 5914 with a filled 24h forward price._

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
| filtered out | 5594 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 91 | -1.34c | -1.00c | 41% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 229 | -1.83c | +0.00c | 43% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 13 | +3.21c | -1.00c | 42% | INSUFFICIENT DATA |
| coordination | 4 | +2.53c | +2.75c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1164 | -0.09c | -0.00c | 52% | NOISE (no measurable edge) |
| large_trade | 1854 | -0.17c | -0.00c | 51% | NOISE (no measurable edge) |
| within_trader | 790 | -0.22c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4742 | -0.29c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 353 | -0.41c | -0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 641 | -0.98c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1389 | -1.58c | -1.00c | 46% | FADE (signal points the wrong way) |
| cross_platform | 94 | -1.96c | +0.00c | 42% | FADE (signal points the wrong way) |
| thin_market | 27 | -1.98c | -0.50c | 38% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 61 | +0.53c | +0.25c | 58% | NOISE (no measurable edge) |
| crypto | 627 | +0.08c | -0.00c | 52% | NOISE (no measurable edge) |
| other | 2780 | -0.43c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2096 | -0.57c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 350 | -0.88c | +0.00c | 49% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 809 | -0.29c | +0.00c | 50% | NOISE (no measurable edge) |
| under 40 | 3610 | -0.31c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 888 | -0.59c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 607 | -1.20c | -0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5273 | -0.37c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 641 | -0.98c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 17 | +5.70c | -0.50c | 47% | INSUFFICIENT DATA |
| 3 to 7 days | 280 | +0.96c | +1.00c | 59% | NOISE (no measurable edge) |
| 1 to 3 days | 224 | +0.20c | +0.35c | 52% | NOISE (no measurable edge) |
| over a month | 3529 | -0.45c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1775 | -0.75c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 125 | -0.49c | 47% |
| p_6h (alerted only) | 117 | -1.08c | 47% |
| p_24h (alerted only) | 91 | -1.34c | 41% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

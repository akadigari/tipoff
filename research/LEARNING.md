# What the scanner has learned about itself

_Auto-generated 2026-07-27T15:49:27Z. 10000 candidates logged, 5973 with a filled 24h forward price._

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
| filtered out | 5647 | -0.44c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 86 | -1.09c | -1.00c | 42% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 240 | -1.59c | -0.00c | 44% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 16 | +3.23c | -0.05c | 47% | INSUFFICIENT DATA |
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1242 | +0.03c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1930 | -0.09c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 839 | -0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4785 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| insiderable | 673 | -0.89c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 349 | -1.15c | -1.00c | 47% | FADE (signal points the wrong way) |
| thin_market | 29 | -1.53c | -0.50c | 41% | INSUFFICIENT DATA |
| price_jump | 1398 | -1.65c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 99 | -2.26c | +0.00c | 40% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 56 | -0.28c | +0.13c | 58% | NOISE (no measurable edge) |
| crypto | 613 | -0.33c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2773 | -0.42c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2142 | -0.54c | +0.00c | 44% | NOISE (no measurable edge) |
| entertainment | 389 | -1.12c | +0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 849 | -0.17c | -0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3600 | -0.42c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 902 | -0.64c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 622 | -1.20c | +0.00c | 49% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5300 | -0.45c | -0.00c | 47% | NOISE (no measurable edge) |
| high | 673 | -0.89c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 21 | +8.30c | +1.95c | 52% | INSUFFICIENT DATA |
| 3 to 7 days | 344 | +0.68c | +0.50c | 56% | NOISE (no measurable edge) |
| 1 to 3 days | 245 | -0.00c | +0.25c | 51% | NOISE (no measurable edge) |
| over a month | 3566 | -0.47c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1696 | -1.03c | -0.05c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 119 | -0.05c | 47% |
| p_6h (alerted only) | 112 | -0.44c | 47% |
| p_24h (alerted only) | 86 | -1.09c | 42% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

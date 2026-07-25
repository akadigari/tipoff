# What the scanner has learned about itself

_Auto-generated 2026-07-25T09:57:54Z. 10000 candidates logged, 5911 with a filled 24h forward price._

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
| filtered out | 5586 | -0.53c | +0.00c | 47% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 98 | -1.61c | -1.00c | 40% | FADE (signal points the wrong way) |
| monitor (strong but gated) | 227 | -1.93c | -0.00c | 42% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 12 | +3.98c | -0.50c | 45% | INSUFFICIENT DATA |
| coordination | 3 | +1.83c | +2.50c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1084 | -0.18c | +0.00c | 50% | NOISE (no measurable edge) |
| within_trader | 767 | -0.20c | +0.00c | 49% | NOISE (no measurable edge) |
| large_trade | 1790 | -0.30c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 4799 | -0.37c | -0.00c | 47% | NOISE (no measurable edge) |
| price_impact | 342 | -0.83c | -0.50c | 48% | NOISE (no measurable edge) |
| insiderable | 602 | -1.06c | +0.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 88 | -2.07c | +0.00c | 42% | FADE (signal points the wrong way) |
| price_jump | 1312 | -2.12c | -1.50c | 44% | FADE (signal points the wrong way) |
| thin_market | 28 | -3.77c | -0.75c | 29% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 60 | +0.58c | +0.40c | 59% | NOISE (no measurable edge) |
| politics | 2089 | -0.54c | +0.00c | 43% | NOISE (no measurable edge) |
| other | 2769 | -0.61c | +0.00c | 47% | NOISE (no measurable edge) |
| crypto | 663 | -0.62c | -0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 330 | -1.07c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3677 | -0.47c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 876 | -0.70c | +0.00c | 46% | NOISE (no measurable edge) |
| 55 to 69 | 791 | -0.78c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 567 | -1.08c | -0.00c | 49% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5309 | -0.55c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 602 | -1.06c | +0.00c | 45% | FADE (signal points the wrong way) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 18 | +3.64c | +1.02c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 235 | +0.66c | +0.75c | 56% | NOISE (no measurable edge) |
| over a month | 3522 | -0.49c | +0.00c | 45% | NOISE (no measurable edge) |
| 1 to 3 days | 204 | -0.77c | -0.50c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1844 | -1.04c | +0.00c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 138 | -0.78c | 45% |
| p_6h (alerted only) | 131 | -1.24c | 47% |
| p_24h (alerted only) | 98 | -1.61c | 40% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

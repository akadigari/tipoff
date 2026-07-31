# What the scanner has learned about itself

_Auto-generated 2026-07-31T17:48:47Z. 10000 candidates logged, 5729 with a filled 24h forward price._

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
| alerted (passed gate and score) | 67 | +0.55c | -0.10c | 48% | NOISE (no measurable edge) |
| filtered out | 5443 | -0.51c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 219 | -1.17c | -0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| coordination | 2 | +2.30c | +2.30c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 14 | +1.96c | +0.32c | 54% | INSUFFICIENT DATA |
| large_trade | 1982 | -0.32c | -0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4662 | -0.35c | +0.00c | 48% | NOISE (no measurable edge) |
| repeat_actor | 1327 | -0.41c | -0.00c | 52% | NOISE (no measurable edge) |
| insiderable | 654 | -0.52c | -0.00c | 48% | NOISE (no measurable edge) |
| within_trader | 846 | -0.75c | +0.00c | 51% | NOISE (no measurable edge) |
| cross_platform | 89 | -1.03c | +0.00c | 49% | FADE (signal points the wrong way) |
| price_impact | 307 | -1.06c | -1.00c | 46% | FADE (signal points the wrong way) |
| thin_market | 41 | -1.42c | -0.45c | 36% | FADE (signal points the wrong way) |
| price_jump | 1245 | -1.56c | -1.00c | 46% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 18 | +0.56c | -0.00c | 47% | INSUFFICIENT DATA |
| crypto | 555 | -0.12c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 370 | -0.15c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2151 | -0.25c | -0.00c | 47% | NOISE (no measurable edge) |
| other | 2635 | -0.88c | +0.00c | 47% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 862 | -0.26c | -0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3419 | -0.41c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 820 | -0.65c | +0.00c | 49% | NOISE (no measurable edge) |
| 70+ | 628 | -1.31c | +0.00c | 50% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5075 | -0.52c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 654 | -0.52c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 26 | +5.41c | +2.92c | 56% | INSUFFICIENT DATA |
| 3 to 7 days | 542 | +0.11c | +0.08c | 51% | NOISE (no measurable edge) |
| over a month | 3555 | -0.33c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1177 | -1.11c | -0.05c | 47% | FADE (signal points the wrong way) |
| 1 to 3 days | 339 | -1.97c | -0.35c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 86 | -0.30c | 44% |
| p_6h (alerted only) | 80 | +0.19c | 51% |
| p_24h (alerted only) | 67 | +0.55c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

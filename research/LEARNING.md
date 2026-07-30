# What the scanner has learned about itself

_Auto-generated 2026-07-30T06:37:15Z. 10000 candidates logged, 5733 with a filled 24h forward price._

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
| filtered out | 5439 | -0.37c | -0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 69 | -0.93c | -1.50c | 42% | NOISE (no measurable edge) |
| monitor (strong but gated) | 225 | -1.09c | +0.00c | 45% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| chatter | 3 | +3.03c | +1.00c | 100% | INSUFFICIENT DATA |
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| fresh_wallet | 16 | +1.46c | -0.05c | 47% | INSUFFICIENT DATA |
| repeat_actor | 1273 | -0.06c | -0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1911 | -0.12c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 835 | -0.24c | +0.00c | 51% | NOISE (no measurable edge) |
| volume_spike | 4653 | -0.24c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 322 | -0.38c | -0.75c | 47% | NOISE (no measurable edge) |
| insiderable | 648 | -0.54c | +0.00c | 48% | NOISE (no measurable edge) |
| thin_market | 38 | -1.39c | -0.15c | 42% | FADE (signal points the wrong way) |
| price_jump | 1257 | -1.48c | -1.00c | 46% | FADE (signal points the wrong way) |
| cross_platform | 94 | -2.21c | +0.00c | 43% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| sports | 21 | +1.19c | +0.00c | 56% | INSUFFICIENT DATA |
| entertainment | 395 | -0.27c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 560 | -0.27c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2147 | -0.35c | -0.00c | 45% | NOISE (no measurable edge) |
| other | 2610 | -0.51c | -0.00c | 48% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 856 | -0.08c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3453 | -0.33c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 824 | -0.69c | +0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 600 | -0.88c | +0.00c | 50% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5085 | -0.39c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 648 | -0.54c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 21 | +10.17c | +7.20c | 62% | INSUFFICIENT DATA |
| 3 to 7 days | 501 | -0.12c | -0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3459 | -0.23c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 3 days | 274 | -0.63c | -0.00c | 50% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1382 | -1.04c | -0.05c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 95 | +0.35c | 48% |
| p_6h (alerted only) | 87 | +0.24c | 52% |
| p_24h (alerted only) | 69 | -0.93c | 42% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

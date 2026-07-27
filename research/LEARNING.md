# What the scanner has learned about itself

_Auto-generated 2026-07-27T19:48:21Z. 10000 candidates logged, 5929 with a filled 24h forward price._

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
| filtered out | 5607 | -0.45c | +0.00c | 48% | NOISE (no measurable edge) |
| alerted (passed gate and score) | 86 | -0.97c | -1.00c | 42% | NOISE (no measurable edge) |
| monitor (strong but gated) | 236 | -1.71c | +0.00c | 42% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 16 | +3.23c | -0.05c | 47% | INSUFFICIENT DATA |
| coordination | 3 | +2.53c | +3.00c | 100% | INSUFFICIENT DATA |
| chatter | 6 | +0.20c | -0.60c | 50% | INSUFFICIENT DATA |
| repeat_actor | 1229 | +0.10c | +0.00c | 53% | NOISE (no measurable edge) |
| large_trade | 1909 | -0.04c | +0.00c | 52% | NOISE (no measurable edge) |
| within_trader | 832 | -0.13c | +0.00c | 52% | NOISE (no measurable edge) |
| volume_spike | 4739 | -0.32c | -0.00c | 47% | NOISE (no measurable edge) |
| insiderable | 673 | -1.00c | +0.00c | 48% | FADE (signal points the wrong way) |
| price_impact | 354 | -1.07c | -1.00c | 47% | FADE (signal points the wrong way) |
| thin_market | 29 | -1.53c | -0.50c | 41% | INSUFFICIENT DATA |
| price_jump | 1394 | -1.80c | -1.00c | 45% | FADE (signal points the wrong way) |
| cross_platform | 97 | -2.78c | -0.05c | 40% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 609 | -0.29c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2757 | -0.41c | +0.00c | 49% | NOISE (no measurable edge) |
| politics | 2113 | -0.56c | +0.00c | 44% | NOISE (no measurable edge) |
| sports | 53 | -0.64c | +0.00c | 57% | NOISE (no measurable edge) |
| entertainment | 397 | -1.25c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 838 | -0.17c | +0.00c | 51% | NOISE (no measurable edge) |
| under 40 | 3578 | -0.42c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 898 | -0.71c | +0.00c | 47% | NOISE (no measurable edge) |
| 70+ | 615 | -1.22c | -0.00c | 49% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5256 | -0.45c | +0.00c | 47% | NOISE (no measurable edge) |
| high | 673 | -1.00c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 22 | +8.63c | +2.90c | 55% | INSUFFICIENT DATA |
| 3 to 7 days | 358 | +0.86c | +0.50c | 56% | NOISE (no measurable edge) |
| 1 to 3 days | 245 | +0.15c | +0.40c | 52% | NOISE (no measurable edge) |
| over a month | 3535 | -0.52c | +0.00c | 46% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1666 | -1.05c | -0.05c | 47% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 119 | -0.12c | 45% |
| p_6h (alerted only) | 110 | -0.53c | 46% |
| p_24h (alerted only) | 86 | -0.97c | 42% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

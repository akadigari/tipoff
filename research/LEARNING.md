# What the scanner has learned about itself

_Auto-generated 2026-08-02T20:15:15Z. 10000 candidates logged, 5836 with a filled 24h forward price._

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
| alerted (passed gate and score) | 63 | -0.42c | -1.00c | 48% | NOISE (no measurable edge) |
| filtered out | 5551 | -0.53c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 222 | -0.66c | +0.00c | 46% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 15 | +2.37c | +0.65c | 60% | INSUFFICIENT DATA |
| coordination | 3 | +1.75c | +0.65c | 100% | INSUFFICIENT DATA |
| volume_spike | 4811 | -0.36c | +0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2034 | -0.40c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1386 | -0.52c | +0.00c | 53% | NOISE (no measurable edge) |
| insiderable | 632 | -0.69c | +0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 842 | -0.86c | -0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 110 | -0.91c | -0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 293 | -1.42c | -1.00c | 45% | FADE (signal points the wrong way) |
| price_jump | 1214 | -1.44c | -1.00c | 47% | FADE (signal points the wrong way) |
| thin_market | 45 | -1.99c | -0.45c | 38% | FADE (signal points the wrong way) |
| chatter | 7 | -11.17c | +0.15c | 57% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 393 | +0.10c | +0.00c | 50% | NOISE (no measurable edge) |
| sports | 18 | -0.11c | -0.00c | 47% | INSUFFICIENT DATA |
| crypto | 554 | -0.24c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2257 | -0.38c | -0.00c | 48% | NOISE (no measurable edge) |
| other | 2614 | -0.83c | -0.00c | 47% | NOISE (no measurable edge) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 875 | -0.35c | -0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3479 | -0.41c | +0.00c | 45% | NOISE (no measurable edge) |
| 40 to 54 | 832 | -0.66c | +0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 650 | -1.31c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5204 | -0.52c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 632 | -0.69c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 25 | +4.23c | +1.95c | 57% | INSUFFICIENT DATA |
| 3 to 7 days | 551 | +0.20c | +0.25c | 52% | NOISE (no measurable edge) |
| over a month | 3777 | -0.38c | -0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1024 | -1.00c | +0.00c | 49% | FADE (signal points the wrong way) |
| 1 to 3 days | 365 | -2.18c | -0.30c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 85 | +0.21c | 45% |
| p_6h (alerted only) | 78 | -1.04c | 44% |
| p_24h (alerted only) | 63 | -0.42c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

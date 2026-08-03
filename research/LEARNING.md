# What the scanner has learned about itself

_Auto-generated 2026-08-03T00:08:28Z. 10000 candidates logged, 5816 with a filled 24h forward price._

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
| alerted (passed gate and score) | 63 | -0.43c | -1.00c | 48% | NOISE (no measurable edge) |
| filtered out | 5527 | -0.45c | -0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 226 | -0.68c | +0.00c | 45% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| fresh_wallet | 15 | +2.37c | +0.65c | 60% | INSUFFICIENT DATA |
| coordination | 4 | +0.96c | +0.63c | 75% | INSUFFICIENT DATA |
| chatter | 10 | +0.66c | +4.47c | 70% | INSUFFICIENT DATA |
| volume_spike | 4798 | -0.29c | -0.00c | 48% | NOISE (no measurable edge) |
| large_trade | 2028 | -0.30c | +0.00c | 54% | NOISE (no measurable edge) |
| repeat_actor | 1388 | -0.36c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 632 | -0.63c | +0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 846 | -0.80c | +0.00c | 53% | NOISE (no measurable edge) |
| cross_platform | 111 | -0.98c | -0.00c | 47% | NOISE (no measurable edge) |
| price_jump | 1209 | -1.24c | -1.00c | 47% | FADE (signal points the wrong way) |
| price_impact | 286 | -1.35c | -1.00c | 45% | FADE (signal points the wrong way) |
| thin_market | 47 | -1.91c | -0.35c | 38% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| entertainment | 382 | +0.24c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 556 | -0.02c | +0.00c | 51% | NOISE (no measurable edge) |
| politics | 2258 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| other | 2600 | -0.79c | +0.00c | 47% | NOISE (no measurable edge) |
| sports | 20 | -0.93c | -0.25c | 41% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 865 | -0.27c | -0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3472 | -0.35c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 822 | -0.64c | +0.00c | 50% | NOISE (no measurable edge) |
| 70+ | 657 | -1.10c | -0.00c | 52% | FADE (signal points the wrong way) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5184 | -0.44c | +0.00c | 48% | NOISE (no measurable edge) |
| high | 632 | -0.63c | +0.00c | 47% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 24 | +6.11c | +2.92c | 59% | INSUFFICIENT DATA |
| 3 to 7 days | 550 | +0.25c | +0.27c | 52% | NOISE (no measurable edge) |
| over a month | 3777 | -0.35c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 4 weeks | 996 | -0.80c | +0.00c | 50% | NOISE (no measurable edge) |
| 1 to 3 days | 373 | -2.00c | -0.25c | 48% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 86 | +0.14c | 43% |
| p_6h (alerted only) | 79 | -1.02c | 44% |
| p_24h (alerted only) | 63 | -0.43c | 48% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

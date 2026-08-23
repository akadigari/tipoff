# What the scanner has learned about itself

_Auto-generated 2026-08-23T03:11:47Z. 10000 candidates logged, 5745 with a filled 24h forward price._

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
| alerted (passed gate and score) | 47 | +2.11c | +1.00c | 57% | FOLLOW |
| filtered out | 5501 | -0.02c | -0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 197 | -0.97c | +0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| price_impact | 258 | +1.58c | -0.00c | 51% | FOLLOW |
| cross_platform | 94 | +1.06c | +0.00c | 51% | FOLLOW |
| price_jump | 759 | -0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| volume_spike | 5102 | -0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| within_trader | 807 | -0.17c | +0.00c | 54% | NOISE (no measurable edge) |
| insiderable | 511 | -0.26c | -0.00c | 45% | NOISE (no measurable edge) |
| coordination | 7 | -0.59c | +0.60c | 83% | INSUFFICIENT DATA |
| large_trade | 1782 | -0.63c | +0.00c | 52% | NOISE (no measurable edge) |
| thin_market | 44 | -0.76c | +0.05c | 57% | NOISE (no measurable edge) |
| repeat_actor | 1305 | -0.78c | -0.00c | 54% | NOISE (no measurable edge) |
| fresh_wallet | 21 | -1.03c | -0.00c | 44% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 1179 | +0.48c | +0.10c | 54% | NOISE (no measurable edge) |
| politics | 2214 | +0.09c | +0.00c | 51% | NOISE (no measurable edge) |
| other | 2259 | -0.36c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 93 | -1.69c | +0.00c | 46% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 40 | 3578 | +0.16c | +0.00c | 47% | NOISE (no measurable edge) |
| 40 to 54 | 729 | +0.11c | -0.00c | 48% | NOISE (no measurable edge) |
| 70+ | 586 | -0.36c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 852 | -0.76c | +0.00c | 53% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5234 | -0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 511 | -0.26c | -0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 40 | +5.26c | +0.00c | 47% | FOLLOW |
| 3 to 7 days | 251 | +0.98c | +0.25c | 53% | NOISE (no measurable edge) |
| over a month | 3608 | +0.01c | +0.00c | 48% | NOISE (no measurable edge) |
| 1 to 3 days | 289 | -0.03c | +0.35c | 55% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1399 | -0.59c | +0.00c | 48% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 88 | +1.45c | 56% |
| p_6h (alerted only) | 76 | +2.59c | 51% |
| p_24h (alerted only) | 47 | +2.11c | 57% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

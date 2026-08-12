# What the scanner has learned about itself

_Auto-generated 2026-08-12T17:08:38Z. 10000 candidates logged, 5647 with a filled 24h forward price._

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
| alerted (passed gate and score) | 86 | +0.71c | +0.00c | 51% | NOISE (no measurable edge) |
| filtered out | 5321 | +0.08c | -0.00c | 50% | NOISE (no measurable edge) |
| monitor (strong but gated) | 240 | -0.82c | +0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 161 | +1.32c | +0.00c | 50% | FOLLOW |
| thin_market | 71 | +1.00c | +0.45c | 65% | FOLLOW |
| fresh_wallet | 23 | +0.72c | -0.05c | 43% | INSUFFICIENT DATA |
| repeat_actor | 1392 | +0.67c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1968 | +0.49c | +0.05c | 56% | NOISE (no measurable edge) |
| within_trader | 833 | +0.36c | +0.10c | 58% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4881 | +0.14c | +0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 874 | -0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 504 | -0.22c | -0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 247 | -0.47c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 5 | -1.15c | -0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2624 | +0.16c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2298 | +0.06c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 523 | -0.08c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 173 | -0.47c | -0.15c | 42% | NOISE (no measurable edge) |
| sports | 29 | -4.83c | -4.50c | 25% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 847 | +0.48c | -0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 800 | +0.40c | +0.00c | 52% | NOISE (no measurable edge) |
| 70+ | 605 | +0.18c | -0.00c | 57% | NOISE (no measurable edge) |
| under 40 | 3395 | -0.15c | +0.00c | 46% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5143 | +0.08c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 504 | -0.22c | -0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 378 | +1.64c | +0.27c | 56% | FOLLOW |
| 1 to 4 weeks | 1307 | +0.34c | -0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 365 | +0.18c | +0.10c | 53% | NOISE (no measurable edge) |
| over a month | 3432 | -0.15c | +0.00c | 46% | NOISE (no measurable edge) |
| under 1 day | 66 | -1.97c | +0.25c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 119 | +0.08c | 48% |
| p_6h (alerted only) | 112 | -1.04c | 42% |
| p_24h (alerted only) | 86 | +0.71c | 51% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

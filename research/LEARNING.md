# What the scanner has learned about itself

_Auto-generated 2026-08-09T22:42:40Z. 10000 candidates logged, 5785 with a filled 24h forward price._

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
| alerted (passed gate and score) | 86 | +1.78c | +1.00c | 55% | FOLLOW |
| filtered out | 5460 | -0.25c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 239 | -0.71c | +0.00c | 51% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 165 | +1.43c | +0.00c | 55% | FOLLOW |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| thin_market | 51 | +0.01c | -0.00c | 56% | NOISE (no measurable edge) |
| repeat_actor | 1350 | -0.09c | +0.05c | 56% | NOISE (no measurable edge) |
| large_trade | 1954 | -0.12c | +0.00c | 55% | NOISE (no measurable edge) |
| volume_spike | 4872 | -0.14c | +0.00c | 49% | NOISE (no measurable edge) |
| price_impact | 283 | -0.35c | -0.50c | 47% | NOISE (no measurable edge) |
| coordination | 2 | -0.37c | -0.37c | 50% | INSUFFICIENT DATA |
| insiderable | 507 | -0.44c | -0.00c | 43% | NOISE (no measurable edge) |
| price_jump | 1031 | -0.52c | -0.50c | 48% | NOISE (no measurable edge) |
| fresh_wallet | 17 | -0.56c | +0.00c | 50% | INSUFFICIENT DATA |
| within_trader | 846 | -0.68c | +0.00c | 55% | NOISE (no measurable edge) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2384 | +0.13c | +0.00c | 50% | NOISE (no measurable edge) |
| entertainment | 265 | +0.09c | +0.00c | 47% | NOISE (no measurable edge) |
| crypto | 515 | -0.27c | +0.00c | 46% | NOISE (no measurable edge) |
| other | 2603 | -0.58c | +0.00c | 48% | NOISE (no measurable edge) |
| sports | 18 | -5.64c | -5.00c | 18% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 40 to 54 | 799 | +0.29c | +0.00c | 53% | NOISE (no measurable edge) |
| 55 to 69 | 847 | -0.09c | +0.00c | 53% | NOISE (no measurable edge) |
| under 40 | 3534 | -0.29c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 605 | -0.84c | -0.00c | 55% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5278 | -0.22c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 507 | -0.44c | -0.00c | 43% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 1 to 4 weeks | 987 | +0.18c | +0.05c | 53% | NOISE (no measurable edge) |
| 3 to 7 days | 484 | +0.14c | -0.00c | 51% | NOISE (no measurable edge) |
| over a month | 3767 | -0.19c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 426 | -1.65c | +0.00c | 50% | FADE (signal points the wrong way) |
| under 1 day | 46 | -5.89c | +0.00c | 50% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 112 | +0.49c | 45% |
| p_6h (alerted only) | 107 | -0.41c | 47% |
| p_24h (alerted only) | 86 | +1.78c | 55% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

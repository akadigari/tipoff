# What the scanner has learned about itself

_Auto-generated 2026-08-21T04:49:16Z. 10000 candidates logged, 5375 with a filled 24h forward price._

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
| alerted (passed gate and score) | 43 | +2.90c | +0.45c | 52% | FOLLOW |
| filtered out | 5160 | -0.16c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 172 | -0.88c | -0.00c | 52% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 9 | +0.86c | +0.60c | 88% | INSUFFICIENT DATA |
| cross_platform | 119 | +0.83c | +0.00c | 47% | NOISE (no measurable edge) |
| within_trader | 715 | +0.08c | -0.00c | 56% | NOISE (no measurable edge) |
| volume_spike | 4739 | +0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| thin_market | 44 | -0.19c | +0.10c | 66% | NOISE (no measurable edge) |
| large_trade | 1590 | -0.27c | +0.00c | 55% | NOISE (no measurable edge) |
| fresh_wallet | 23 | -0.29c | +0.05c | 60% | INSUFFICIENT DATA |
| repeat_actor | 1148 | -0.32c | +0.05c | 56% | NOISE (no measurable edge) |
| insiderable | 457 | -0.43c | +0.00c | 45% | NOISE (no measurable edge) |
| price_impact | 217 | -0.51c | -0.50c | 46% | NOISE (no measurable edge) |
| price_jump | 720 | -1.25c | -0.78c | 47% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| politics | 2386 | -0.00c | +0.00c | 49% | NOISE (no measurable edge) |
| crypto | 842 | -0.04c | +0.10c | 56% | NOISE (no measurable edge) |
| other | 2040 | -0.29c | +0.00c | 45% | NOISE (no measurable edge) |
| entertainment | 107 | -2.11c | -1.00c | 42% | FADE (signal points the wrong way) |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 70+ | 488 | +0.13c | +0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3431 | -0.10c | +0.00c | 46% | NOISE (no measurable edge) |
| 40 to 54 | 688 | -0.11c | +0.00c | 48% | NOISE (no measurable edge) |
| 55 to 69 | 768 | -0.65c | +0.00c | 55% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 4918 | -0.13c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 457 | -0.43c | +0.00c | 45% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| under 1 day | 53 | +4.49c | +0.00c | 49% | FOLLOW |
| over a month | 3432 | -0.10c | -0.00c | 47% | NOISE (no measurable edge) |
| 3 to 7 days | 238 | -0.37c | +0.23c | 53% | NOISE (no measurable edge) |
| 1 to 4 weeks | 1230 | -0.49c | +0.00c | 49% | NOISE (no measurable edge) |
| 1 to 3 days | 287 | -0.85c | +0.15c | 54% | NOISE (no measurable edge) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 78 | +2.54c | 56% |
| p_6h (alerted only) | 68 | +3.07c | 56% |
| p_24h (alerted only) | 43 | +2.90c | 52% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

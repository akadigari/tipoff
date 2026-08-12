# What the scanner has learned about itself

_Auto-generated 2026-08-12T16:05:54Z. 10000 candidates logged, 5626 with a filled 24h forward price._

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
| alerted (passed gate and score) | 85 | +0.65c | -0.00c | 50% | NOISE (no measurable edge) |
| filtered out | 5299 | +0.08c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 242 | -0.99c | +0.00c | 48% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 163 | +1.27c | +0.00c | 49% | FOLLOW |
| thin_market | 71 | +1.00c | +0.45c | 65% | FOLLOW |
| fresh_wallet | 23 | +0.81c | +0.00c | 48% | INSUFFICIENT DATA |
| repeat_actor | 1383 | +0.62c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1959 | +0.49c | +0.05c | 56% | NOISE (no measurable edge) |
| within_trader | 829 | +0.40c | +0.10c | 58% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4861 | +0.12c | -0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 869 | -0.08c | -0.10c | 49% | NOISE (no measurable edge) |
| insiderable | 504 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 251 | -0.46c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 5 | -1.15c | -0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2611 | +0.16c | +0.00c | 50% | NOISE (no measurable edge) |
| politics | 2303 | +0.01c | +0.00c | 50% | NOISE (no measurable edge) |
| crypto | 506 | -0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| entertainment | 177 | -0.15c | +0.00c | 43% | NOISE (no measurable edge) |
| sports | 29 | -4.83c | -4.50c | 25% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 844 | +0.53c | -0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 798 | +0.36c | -0.00c | 52% | NOISE (no measurable edge) |
| 70+ | 604 | +0.06c | -0.00c | 56% | NOISE (no measurable edge) |
| under 40 | 3380 | -0.16c | +0.00c | 46% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5122 | +0.07c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 504 | -0.27c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 376 | +1.56c | +0.25c | 56% | FOLLOW |
| 1 to 4 weeks | 1290 | +0.36c | +0.00c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 368 | +0.16c | +0.10c | 53% | NOISE (no measurable edge) |
| over a month | 3428 | -0.16c | +0.00c | 46% | NOISE (no measurable edge) |
| under 1 day | 67 | -1.94c | +0.20c | 53% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 117 | +0.09c | 48% |
| p_6h (alerted only) | 112 | -1.04c | 42% |
| p_24h (alerted only) | 85 | +0.65c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

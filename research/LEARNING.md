# What the scanner has learned about itself

_Auto-generated 2026-08-08T15:38:23Z. 10000 candidates logged, 5687 with a filled 24h forward price._

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
| alerted (passed gate and score) | 79 | +1.10c | +1.00c | 55% | FOLLOW |
| filtered out | 5378 | -0.30c | +0.00c | 48% | NOISE (no measurable edge) |
| monitor (strong but gated) | 230 | -0.60c | +0.00c | 50% | NOISE (no measurable edge) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| coordination | 3 | +1.08c | +0.65c | 67% | INSUFFICIENT DATA |
| cross_platform | 152 | +0.17c | +0.00c | 49% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| large_trade | 1979 | -0.16c | +0.00c | 55% | NOISE (no measurable edge) |
| repeat_actor | 1368 | -0.18c | +0.05c | 55% | NOISE (no measurable edge) |
| volume_spike | 4745 | -0.23c | +0.00c | 49% | NOISE (no measurable edge) |
| fresh_wallet | 20 | -0.28c | +0.07c | 53% | INSUFFICIENT DATA |
| insiderable | 538 | -0.29c | +0.00c | 48% | NOISE (no measurable edge) |
| price_jump | 1080 | -0.43c | -0.05c | 49% | NOISE (no measurable edge) |
| price_impact | 276 | -0.71c | -0.80c | 46% | NOISE (no measurable edge) |
| within_trader | 839 | -0.73c | +0.00c | 55% | NOISE (no measurable edge) |
| thin_market | 42 | -1.10c | -0.00c | 47% | FADE (signal points the wrong way) |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| crypto | 502 | -0.04c | +0.00c | 47% | NOISE (no measurable edge) |
| entertainment | 322 | -0.11c | +0.00c | 46% | NOISE (no measurable edge) |
| politics | 2324 | -0.12c | +0.00c | 49% | NOISE (no measurable edge) |
| other | 2522 | -0.49c | +0.00c | 49% | NOISE (no measurable edge) |
| sports | 17 | -5.85c | -5.50c | 19% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 862 | -0.04c | +0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 789 | -0.11c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3415 | -0.28c | +0.00c | 45% | NOISE (no measurable edge) |
| 70+ | 621 | -0.92c | +0.00c | 54% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5149 | -0.29c | +0.00c | 49% | NOISE (no measurable edge) |
| high | 538 | -0.29c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 550 | +0.43c | +0.30c | 52% | NOISE (no measurable edge) |
| 1 to 4 weeks | 874 | -0.12c | -0.00c | 52% | NOISE (no measurable edge) |
| over a month | 3749 | -0.25c | +0.00c | 47% | NOISE (no measurable edge) |
| 1 to 3 days | 393 | -1.85c | -0.10c | 49% | FADE (signal points the wrong way) |
| under 1 day | 35 | -4.53c | +0.30c | 58% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 108 | +0.53c | 46% |
| p_6h (alerted only) | 104 | -0.88c | 44% |
| p_24h (alerted only) | 79 | +1.10c | 55% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

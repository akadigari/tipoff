# What the scanner has learned about itself

_Auto-generated 2026-08-12T11:55:07Z. 10000 candidates logged, 5708 with a filled 24h forward price._

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
| filtered out | 5381 | +0.09c | +0.00c | 49% | NOISE (no measurable edge) |
| monitor (strong but gated) | 242 | -1.14c | +0.00c | 48% | FADE (signal points the wrong way) |

## Per trigger

A trigger that reads FADE is pointing the wrong way and is a candidate for inverting or dropping.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| cross_platform | 169 | +1.20c | +0.00c | 49% | FOLLOW |
| thin_market | 70 | +1.02c | +0.47c | 66% | FOLLOW |
| fresh_wallet | 23 | +0.81c | +0.00c | 48% | INSUFFICIENT DATA |
| repeat_actor | 1390 | +0.61c | +0.10c | 57% | NOISE (no measurable edge) |
| large_trade | 1965 | +0.47c | +0.05c | 56% | NOISE (no measurable edge) |
| within_trader | 836 | +0.32c | +0.10c | 58% | NOISE (no measurable edge) |
| chatter | 10 | +0.16c | +2.00c | 67% | INSUFFICIENT DATA |
| volume_spike | 4925 | +0.10c | -0.00c | 50% | NOISE (no measurable edge) |
| price_jump | 899 | +0.09c | -0.00c | 49% | NOISE (no measurable edge) |
| insiderable | 510 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |
| price_impact | 258 | -0.88c | -0.50c | 46% | NOISE (no measurable edge) |
| coordination | 5 | -1.15c | -0.00c | 50% | INSUFFICIENT DATA |

## Per category

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| other | 2648 | +0.19c | +0.00c | 51% | NOISE (no measurable edge) |
| crypto | 509 | +0.05c | +0.00c | 48% | NOISE (no measurable edge) |
| politics | 2340 | +0.01c | +0.00c | 49% | NOISE (no measurable edge) |
| entertainment | 182 | -0.70c | -0.10c | 42% | NOISE (no measurable edge) |
| sports | 29 | -4.83c | -4.50c | 25% | INSUFFICIENT DATA |

## Per score band

These should improve as the score rises. If they do not, the point weights are wrong.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 55 to 69 | 847 | +0.57c | -0.00c | 54% | NOISE (no measurable edge) |
| 40 to 54 | 806 | +0.47c | +0.00c | 52% | NOISE (no measurable edge) |
| under 40 | 3439 | -0.15c | -0.00c | 46% | NOISE (no measurable edge) |
| 70+ | 616 | -0.16c | +0.00c | 56% | NOISE (no measurable edge) |

## Per insiderability tier

'high' means a market that resolves on a private human decision.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| normal | 5198 | +0.08c | +0.00c | 50% | NOISE (no measurable edge) |
| high | 510 | -0.32c | +0.00c | 48% | NOISE (no measurable edge) |

## Per time-to-resolution (the accurate-time-to-bet table)

Sorted by average, but read it in time order too. The strongest timing lever in the data: near-resolution signals pay, far-out ones do not. Informed money shows up when the event is imminent; a spike months out is rumor churn. This is why the gate now caps at 30 days.

| Bucket | Samples | Avg move | Median | Moved our way | Verdict |
|---|---|---|---|---|---|
| 3 to 7 days | 375 | +1.48c | +0.25c | 56% | FOLLOW |
| 1 to 4 weeks | 1277 | +0.44c | +0.05c | 53% | NOISE (no measurable edge) |
| 1 to 3 days | 371 | +0.26c | +0.10c | 52% | NOISE (no measurable edge) |
| over a month | 3519 | -0.16c | +0.00c | 46% | NOISE (no measurable edge) |
| under 1 day | 70 | -2.86c | +0.03c | 51% | FADE (signal points the wrong way) |

## Horizon check

| Horizon | Samples | Avg move | Moved our way |
|---|---|---|---|
| p_1h (alerted only) | 116 | +0.25c | 48% |
| p_6h (alerted only) | 111 | -1.07c | 42% |
| p_24h (alerted only) | 85 | +0.65c | 50% |

## How to act on this

1. A trigger with a FADE verdict and a real sample is the
   clearest finding available. Either invert it or drop it.
2. If score bands do not climb, rebalance the points in
   config.py toward whichever triggers actually earn.
3. Anything still reading INSUFFICIENT DATA stays untouched.
   Waiting is cheaper than learning noise.

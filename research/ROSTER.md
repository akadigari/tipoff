# Wallet roster

_Auto-generated 2026-08-17T22:34:17Z. 1211 flagged wallets, 13 with enough graded trades to judge, 2 that beat a coin flip._

Each wallet is graded on the price move that followed its flagged
trades, in the wallet's own direction, using data the scanner
already collected. A wallet earns WATCH only with at least
12 graded moves, a positive average, and a hit rate that
beats a coin flip (p < 0.05). Averages are in cents of probability.

**Read this before trusting the list.** These wallets were surfaced
by detectors the self-audit (LEARNING.md) calls noise, so the pool
leans toward market makers and busy whales, not quiet insiders. A
high flag count is a reason for suspicion, not trust: real insiders
in the documented cases traded once, in one market, then vanished.
The grading below is exactly what separates the two.

## Watch list (earned it)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 23 | +3.57c | 75% | 0.02 | 12 | 49 | WATCH (beats luck) |
| `0xe734e7bf7c...` | 22 | +2.32c | 77% | 0.01 | 8 | 102 | WATCH (beats luck) |

## Promising (edge, needs more data to rule out luck)

_None yet._

## Top of the pack by average (all verdicts)

| Wallet | Graded | Avg move | Hit rate | Luck p | Markets | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| `0xfc2f4f50ce...` | 23 | +3.57c | 75% | 0.02 | 12 | 49 | WATCH (beats luck) |
| `0xe734e7bf7c...` | 22 | +2.32c | 77% | 0.01 | 8 | 102 | WATCH (beats luck) |
| `0xeb490d0534...` | 26 | +0.85c | 62% | 0.15 | 14 | 43 | NOISE (busy, not sharp) |
| `0x74471a007d...` | 12 | +0.39c | 50% | 0.61 | 9 | 54 | NOISE (busy, not sharp) |
| `0x06dc51826b...` | 28 | +0.33c | 67% | 0.06 | 25 | 133 | NOISE (busy, not sharp) |
| `0x3eae57986b...` | 17 | +0.24c | 64% | 0.21 | 17 | 45 | NOISE (busy, not sharp) |
| `0x000d257d2d...` | 14 | +0.22c | 46% | 0.71 | 13 | 24 | NOISE (busy, not sharp) |
| `0x122cb94c43...` | 26 | -0.02c | 52% | 0.50 | 34 | 96 | NOISE (busy, not sharp) |
| `0x6765c1c000...` | 12 | -0.11c | 80% | 0.06 | 6 | 30 | NOISE (busy, not sharp) |
| `0xdf44c3e8ce...` | 13 | -0.32c | 50% | 0.61 | 11 | 18 | NOISE (busy, not sharp) |
| `0xdf17f4a8dd...` | 13 | -1.15c | 67% | 0.19 | 17 | 37 | FADE (bets the wrong way) |
| `0x6d9fc316c3...` | 14 | -2.21c | 29% | 0.97 | 11 | 47 | FADE (bets the wrong way) |
| `0xb10047d6a2...` | 23 | -3.95c | 43% | 0.81 | 20 | 57 | FADE (bets the wrong way) |

## Documented known insiders (Phase B watch targets)

Publicly-reported insider wallets from the backtest episodes, by the pseudonym the reporting used. On-chain addresses still need resolving before they can be watched live, and most are likely burned (insiders rotate addresses). Tripwires, not a strategy.

| Pseudonym | Episode |
|---|---|
| 6741 | Nobel Peace Prize 2025 leak (Machado) |
| dirtycup | Nobel Peace Prize 2025 leak (Machado) |
| Magamyman | US strike on Iran, Feb 2026 (six fresh wallets) |
| Planktonbets | US strike on Iran, Feb 2026 |
| bigwinner01 | Trump pardons CZ, Oct 2025 |
| romanticpaul | Taylor Swift engagement, Aug 2025 |
| ricosuave666 | IAF reservist / Rising Lion, June 2025 (indicted) |

## Next step

If the watch list stays empty or tiny once normal mode fills the
data, wallet-first is not worth the API budget and we do not build
Phase B. If real names keep earning WATCH, Phase B polls those
wallets every run and alerts the moment they open a new position,
before the market is anomalous.
